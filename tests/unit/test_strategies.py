import pytest
import fitz
from src.domain.enums import DataType, RuleType, SearchMode, Direction
from src.domain.models import AnchorExtractionRule, BoundingBoxExtractionRule, BoundingBox
from src.strategies.anchor_strategy import AnchorExtractionStrategy
from src.strategies.bounding_box_strategy import BoundingBoxExtractionStrategy
from src.services.pdf_service import PdfService

# Mock fitz Document and Page
class MockPage:
    def __init__(self, blocks, width=600, height=800):
        self.blocks = blocks
        self.rect = fitz.Rect(0, 0, width, height)

    def search_for(self, text):
        rects = []
        for b in self.blocks:
            if text in b[4]:
                rects.append(fitz.Rect(b[0], b[1], b[2], b[3]))
        return rects

    def get_text(self, option, clip=None):
        if option == "blocks":
            # format: (x0, y0, x1, y1, "text", block_no, block_type)
            return [(b[0], b[1], b[2], b[3], b[4], i, 0) for i, b in enumerate(self.blocks)]
        elif option == "words":
            # format: (x0, y0, x1, y1, "word", block_no, line_no, word_no)
            return [(b[0], b[1], b[2], b[3], b[4], i, 0, 0) for i, b in enumerate(self.blocks)]
        elif option == "text":
            if clip:
                # simple mock logic for clip
                result = []
                for b in self.blocks:
                    # check intersection roughly
                    b_rect = fitz.Rect(b[0], b[1], b[2], b[3])
                    if clip.intersects(b_rect):
                        result.append(b[4])
                return "\n".join(result)
            return ""

class MockDocument:
    def __init__(self, pages):
        self.pages = pages
        
    def __len__(self):
        return len(self.pages)
        
    def __getitem__(self, idx):
        return self.pages[idx]

@pytest.fixture
def sample_pdf():
    # Blocks: x0, y0, x1, y1, text
    blocks = [
        (50, 50, 150, 70, "Invoice Total:"),
        (160, 50, 250, 70, "$1,000.00"),
        (50, 100, 150, 120, "Vendor:"),
        (50, 130, 200, 150, "Acme Corp")
    ]
    page = MockPage(blocks)
    return MockDocument([page])

def test_anchor_strategy_exact_right(sample_pdf, monkeypatch):
    # Mock the static methods in PdfService since we use them in strategies
    monkeypatch.setattr(PdfService, "get_text_blocks", lambda doc, p: [
        {"rect": fitz.Rect(b[0], b[1], b[2], b[3]), "text": b[4]} 
        for b in sample_pdf.pages[p].blocks
    ])

    rule = AnchorExtractionRule(
        key_name="total",
        data_type=DataType.CURRENCY,
        anchor_text="Invoice Total:",
        search_mode=SearchMode.EXACT,
        direction=Direction.RIGHT,
        offset_distance=100.0
    )
    strategy = AnchorExtractionStrategy(rule)
    result = strategy.extract(sample_pdf, 0)
    
    assert result == "$1,000.00"

def test_anchor_strategy_pseudo_bolding_and_artifact_overlap():
    blocks = [
        # Anchor text pseudo bolding (3 exact same rects overlapping)
        (100, 200, 150, 210, "Your Score:"),
        (100, 200, 150, 210, "Your Score:"),
        (100, 200, 150, 210, "Your Score:"),
        # The correct target value to the right
        (160, 200, 180, 210, "844"),
        # A tiny artifact on the same X as target but height is tiny and overlaps the top
        (160, 200, 180, 201, "700"),
    ]
    page = MockPage(blocks)
    doc = MockDocument([page])

    rule = AnchorExtractionRule(
        key_name="score",
        data_type=DataType.NUMBER,
        anchor_text="Your Score:",
        search_mode=SearchMode.EXACT,
        direction=Direction.RIGHT,
        offset_distance=100.0
    )
    strategy = AnchorExtractionStrategy(rule)
    result = strategy.extract(doc, 0)
    
    # 700 should be ignored because its overlap (1 point) is not > 50% of anchor.height (10 points)
    assert result == "844"

def test_bounding_box_strategy(sample_pdf, monkeypatch):
    monkeypatch.setattr(PdfService, "get_page_dimensions", lambda doc, p: (
        0.0, 0.0, doc.pages[p].rect.width, doc.pages[p].rect.height
    ))

    # Box around Vendor Acme Corp (50, 100) -> (200, 150)
    # x_pct = 50/600 = 0.0833
    # y_pct = 100/800 = 0.125
    # w_pct = 150/600 = 0.25
    # h_pct = 50/800 = 0.0625
    box = BoundingBox(x_pct=0.08, y_pct=0.12, width_pct=0.26, height_pct=0.07)
    
    rule = BoundingBoxExtractionRule(
        key_name="vendor",
        data_type=DataType.STRING,
        box=box
    )
    
    strategy = BoundingBoxExtractionStrategy(rule)
    result = strategy.extract(sample_pdf, 0)
    
    assert "Vendor:" in result
    assert "Acme Corp" in result

def test_anchor_strategy_exact_substring_avoidance():
    # Test that searching for "Date:" doesn't accidentally match "Candidate:"
    blocks = [
        (100, 100, 200, 110, "Candidate:"),
        (210, 100, 250, 110, "Bob"),
        (100, 150, 150, 160, "Date:"),
        (160, 150, 200, 160, "Oct 21")
    ]
    page = MockPage(blocks)
    doc = MockDocument([page])
    
    rule = AnchorExtractionRule(
        key_name="date",
        data_type=DataType.STRING,
        anchor_text="Date:",
        search_mode=SearchMode.EXACT,
        direction=Direction.RIGHT,
        offset_distance=100.0
    )
    strategy = AnchorExtractionStrategy(rule)
    result = strategy.extract(doc, 0)
    
    assert result == "Oct 21"

def test_anchor_strategy_horizontal_sort_respects_y():
    # Test that words are sorted by Y first, then X, to handle multi-line words
    blocks = [
        (100, 150, 150, 160, "Date:"),
        # 2022 has a smaller X (160) than Friday (170), but a larger Y (154 vs 150)
        # They overlap in Y (>50% of anchor.height)
        (160, 154, 180, 164, "2022"),
        (170, 148, 220, 158, "Friday,"),
        (230, 148, 270, 158, "Oct 21,")
    ]
    page = MockPage(blocks)
    doc = MockDocument([page])
    
    rule = AnchorExtractionRule(
        key_name="date",
        data_type=DataType.STRING,
        anchor_text="Date:",
        search_mode=SearchMode.EXACT,
        direction=Direction.RIGHT,
        offset_distance=200.0
    )
    strategy = AnchorExtractionStrategy(rule)
    result = strategy.extract(doc, 0)
    
    assert result == "Friday, Oct 21, 2022"
