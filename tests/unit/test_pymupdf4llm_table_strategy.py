"""
Unit tests for PyMuPDF4LLM table extraction path and markdown table parser.
"""
import pytest
import pymupdf as fitz
from src.domain.models import TableExtractionRule, BoundingBox
from src.domain.enums import TableBoundaryType, TableEngine
from src.strategies.table_strategy import TableExtractionStrategy, _parse_markdown_table


class TestMarkdownTableParser:
    def test_parse_basic_table(self):
        md = """
| Name   | Qty | Price |
|--------|-----|-------|
| Widget |  1  | $10   |
| Gadget |  2  | $20   |
"""
        result = _parse_markdown_table(md)
        assert len(result) == 3  # header + 2 data rows
        assert result[0] == ["Name", "Qty", "Price"]
        assert result[1][0] == "Widget"
        assert result[2][0] == "Gadget"

    def test_parse_no_table_returns_empty(self):
        md = "This is plain text with no table."
        result = _parse_markdown_table(md)
        assert result == []

    def test_parse_table_without_separator(self):
        md = """
| A | B |
| 1 | 2 |
| 3 | 4 |
"""
        result = _parse_markdown_table(md)
        assert len(result) == 3  # All three rows (no separator to skip)

    def test_parse_table_with_extra_whitespace(self):
        md = "|  Col A  |  Col B  |\n|---------|----------|\n|  val1   |  val2   |"
        result = _parse_markdown_table(md)
        assert any("Col A" in row[0] for row in result)
        assert any("val1" in row[0] for row in result)

    def test_normalize_into_list_of_lists(self):
        md = "| H1 | H2 | H3 |\n|---|---|---|\n| a | b | c |"
        result = _parse_markdown_table(md)
        assert isinstance(result, list)
        assert all(isinstance(row, list) for row in result)
        assert result[-1] == ["a", "b", "c"]


class TestPyMuPDF4LLMExtraction:
    def _make_bordered_table_pdf(self, tmp_path) -> str:
        """Create a PDF with a simple bordered table."""
        path = str(tmp_path / "table.pdf")
        doc = fitz.open()
        page = doc.new_page()

        # Draw a simple 2-column, 3-row table using rectangles + text
        col_widths = [200, 100]
        row_height = 20
        x0, y0 = 72, 100

        headers = [("Item", "Price")]
        rows = [("Widget", "$10"), ("Gadget", "$20")]
        all_rows = headers + rows

        for ri, row in enumerate(all_rows):
            cx = x0
            for ci, cell in enumerate(row):
                rect = fitz.Rect(cx, y0 + ri * row_height, cx + col_widths[ci], y0 + (ri + 1) * row_height)
                page.draw_rect(rect)
                page.insert_text((cx + 5, y0 + ri * row_height + 14), cell, fontsize=10)
                cx += col_widths[ci]

        doc.save(path)
        doc.close()
        return path

    def test_pymupdf4llm_engine_does_not_crash(self, tmp_path):
        """Even if no markdown table is found, engine should fall back gracefully."""
        pdf = self._make_bordered_table_pdf(tmp_path)
        rule = TableExtractionRule(
            key_name="items",
            data_type="STRING",
            boundary_type=TableBoundaryType.BOUNDING_BOX,
            box=BoundingBox(x_pct=0.0, y_pct=0.0, width_pct=1.0, height_pct=1.0),
            page_index=0,
        )
        # Override engine to pymupdf4llm
        rule.config.engine = TableEngine.PYMUPDF4LLM
        strategy = TableExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        # Should not raise — result is a list or dict
        assert isinstance(result, (list, dict))

    def test_native_pymupdf_engine_still_works(self, tmp_path):
        """PyMuPDF native engine path is unaffected after refactoring."""
        pdf = self._make_bordered_table_pdf(tmp_path)
        rule = TableExtractionRule(
            key_name="items",
            data_type="STRING",
            boundary_type=TableBoundaryType.BOUNDING_BOX,
            box=BoundingBox(x_pct=0.0, y_pct=0.0, width_pct=1.0, height_pct=1.0),
            page_index=0,
        )
        rule.config.engine = TableEngine.PYMUPDF
        strategy = TableExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        assert isinstance(result, (list, dict))

    def test_key_value_mapping(self):
        """Verify that extract_as_key_value flattens a 2-column table."""
        rows = [["Item", "Price"], ["Widget", "$10"], ["Gadget", "$20"]]
        from src.domain.models import TableConfig
        from src.domain.enums import TableEngine
        config = TableConfig(extract_as_key_value=True, engine=TableEngine.PYMUPDF)
        rule = TableExtractionRule(
            key_name="kv",
            data_type="STRING",
            box=BoundingBox(x_pct=0, y_pct=0, width_pct=1, height_pct=1),
            config=config,
        )
        strategy = TableExtractionStrategy(rule)
        result = strategy._post_process(rows)
        assert isinstance(result, dict)
        assert "Widget" in result
        assert result["Widget"] == "$10"
