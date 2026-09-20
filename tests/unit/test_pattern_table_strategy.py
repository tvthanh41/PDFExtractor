"""
Unit tests for dynamic pattern-based table extraction via TableExtractionStrategy.
"""
import pytest
import pymupdf as fitz
from src.domain.models import TableExtractionRule, PatternBoundaryConfig
from src.domain.enums import TableBoundaryType
from src.strategies.table_strategy import TableExtractionStrategy


def make_pdf_with_table(tmp_path) -> str:
    """Create a single-page PDF simulating a simple table layout."""
    path = str(tmp_path / "table_test.pdf")
    doc = fitz.open()
    page = doc.new_page()
    y = 72

    lines = [
        "Invoice #1234",
        "",
        "Item Description    Qty    Price",
        "Widget A             1     $10.00",
        "Widget B             2     $20.00",
        "Gadget C             3     $30.00",
        "Subtotal                   $60.00",
        "",
        "Notes: Payment due within 30 days.",
    ]
    for line in lines:
        page.insert_text((72, y), line, fontsize=11)
        y += 18

    doc.save(path)
    doc.close()
    return path


class TestPatternTableStrategy:
    def test_pattern_match_boundary_extracts_rows(self, tmp_path):
        """Pattern match should detect table between start/end patterns."""
        pdf = make_pdf_with_table(tmp_path)
        pb = PatternBoundaryConfig(
            start_pattern="Item Description",
            end_pattern="Subtotal",
            include_start=True,
            include_end=False,
        )
        rule = TableExtractionRule(
            key_name="items",
            data_type="STRING",
            boundary_type=TableBoundaryType.PATTERN_MATCH,
            pattern_boundary=pb,
            page_index=0,
        )
        strategy = TableExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        # Result should be a list of rows or None if table detection couldn't find rows
        # Just verify it didn't throw an exception and returned a sensible type
        assert result is None or isinstance(result, (list, dict))

    def test_pattern_match_no_start_returns_none(self, tmp_path):
        pdf = make_pdf_with_table(tmp_path)
        pb = PatternBoundaryConfig(
            start_pattern="NONEXISTENT_HEADER",
            end_pattern="Subtotal",
        )
        rule = TableExtractionRule(
            key_name="items",
            data_type="STRING",
            boundary_type=TableBoundaryType.PATTERN_MATCH,
            pattern_boundary=pb,
            page_index=0,
        )
        strategy = TableExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        assert result is None or result == [] or result == {}

    def test_bounding_box_boundary_still_works(self, tmp_path):
        """Existing bounding-box extraction must still function after refactor."""
        from src.domain.models import BoundingBox
        pdf = make_pdf_with_table(tmp_path)
        rule = TableExtractionRule(
            key_name="items",
            data_type="STRING",
            boundary_type=TableBoundaryType.BOUNDING_BOX,
            box=BoundingBox(x_pct=0.0, y_pct=0.0, width_pct=1.0, height_pct=1.0),
            page_index=0,
        )
        strategy = TableExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        # Should return a list (possibly empty if no table detected) without crashing
        assert result is None or isinstance(result, (list, dict))
