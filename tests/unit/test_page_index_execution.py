"""
Unit tests verifying that extraction rules correctly use page_index
when executing against multi-page documents.
"""
import pytest
import pymupdf as fitz
from src.domain.models import AnchorExtractionRule, BoundingBox, BoundingBoxExtractionRule, TableExtractionRule
from src.strategies.anchor_strategy import AnchorExtractionStrategy
from src.strategies.bounding_box_strategy import BoundingBoxExtractionStrategy


def make_multipage_pdf(tmp_path, pages_content: list[str]) -> str:
    """Create a multi-page PDF where each page has specific text."""
    path = str(tmp_path / "multipage.pdf")
    doc = fitz.open()
    for text in pages_content:
        page = doc.new_page()
        page.insert_text((72, 100), text, fontsize=12)
    doc.save(path)
    doc.close()
    return path


class TestAnchorPageIndexExecution:
    def test_anchor_on_page_0(self, tmp_path):
        pdf = make_multipage_pdf(tmp_path, ["InvoiceDate: 2024-01-01", "OtherDate: 2024-06-01"])
        rule = AnchorExtractionRule(
            key_name="date",
            data_type="STRING",
            anchor_text="InvoiceDate:",
            page_index=0,
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        assert result is not None
        assert "2024-01-01" in result

    def test_anchor_on_page_1(self, tmp_path):
        pdf = make_multipage_pdf(tmp_path, ["InvoiceDate: 2024-01-01", "OtherDate: 2024-06-01"])
        rule = AnchorExtractionRule(
            key_name="other_date",
            data_type="STRING",
            anchor_text="OtherDate:",
            page_index=1,
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 1)
        doc.close()
        assert result is not None
        assert "2024-06-01" in result

    def test_anchor_wrong_page_returns_none(self, tmp_path):
        """Anchor on page 0 text should return None when extracted from page 1."""
        pdf = make_multipage_pdf(tmp_path, ["InvoiceDate: 2024-01-01", "OtherPage text"])
        rule = AnchorExtractionRule(
            key_name="date",
            data_type="STRING",
            anchor_text="InvoiceDate:",
            page_index=0,
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        # Extracting from page 1 where anchor doesn't exist
        result = strategy.extract(doc, 1)
        doc.close()
        assert result is None

    def test_out_of_range_page_returns_none(self, tmp_path):
        pdf = make_multipage_pdf(tmp_path, ["Page 0"])
        rule = AnchorExtractionRule(
            key_name="x",
            data_type="STRING",
            anchor_text="Page",
            page_index=0,
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 999)
        doc.close()
        assert result is None


class TestBoundingBoxPageIndexExecution:
    def test_bbox_rule_on_correct_page(self, tmp_path):
        pdf = make_multipage_pdf(tmp_path, ["Amount 500.00", "Amount 999.00"])
        rule = BoundingBoxExtractionRule(
            key_name="amount",
            data_type="STRING",
            page_index=1,
            box=BoundingBox(x_pct=0.0, y_pct=0.0, width_pct=1.0, height_pct=1.0),
        )
        strategy = BoundingBoxExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 1)
        doc.close()
        assert result is not None
        assert "999" in result
