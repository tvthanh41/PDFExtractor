import pytest
import pymupdf as fitz
import os
from src.domain.enums import DataType, SearchMode, Direction
from src.domain.models import AnchorExtractionRule
from src.strategies.anchor_strategy import AnchorExtractionStrategy

@pytest.fixture
def real_pdf_doc():
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "..", "sample", "scorereport.pdf")
    if not os.path.exists(pdf_path):
        pytest.skip(f"sample/scorereport.pdf not found at {pdf_path}")
    
    doc = fitz.open(pdf_path)
    yield doc
    doc.close()

def test_real_pdf_date_extraction(real_pdf_doc):
    # This tests the bug where "Date:" matched the substring inside "Candidate:"
    # and the horizontal grouping didn't handle line wrapping for "2022"
    rule = AnchorExtractionRule(
        key_name="date",
        data_type=DataType.STRING,
        anchor_text="Date:",
        search_mode=SearchMode.EXACT,
        direction=Direction.RIGHT,
        offset_distance=300.0
    )
    strategy = AnchorExtractionStrategy(rule)
    result = strategy.extract(real_pdf_doc, 0)
    
    assert result == "Friday, October 21, 2022"

def test_real_pdf_score_extraction(real_pdf_doc):
    # This tests the bug where invisible artifacts (like "Passing") overlapping with "Your Score:" 
    # ruined the exact matching logic
    rule = AnchorExtractionRule(
        key_name="score",
        data_type=DataType.NUMBER,
        anchor_text="Your Score:",
        search_mode=SearchMode.EXACT,
        direction=Direction.RIGHT,
        offset_distance=300.0
    )
    strategy = AnchorExtractionStrategy(rule)
    result = strategy.extract(real_pdf_doc, 0)
    
    assert result == "844"
