"""
Unit tests for AnchorExtractionStrategy with:
- Multi-page page_index enforcement
- skip_k (match_index) occurrence selection
- Exact, case-insensitive, and regex search modes
"""
import pytest
import pymupdf as fitz
from src.domain.models import AnchorExtractionRule
from src.domain.enums import SearchMode, Direction
from src.strategies.anchor_strategy import AnchorExtractionStrategy


def make_pdf(tmp_path, pages_content: list[str]) -> str:
    """Create multi-page PDF with one text block per page."""
    path = str(tmp_path / "anchor_test.pdf")
    doc = fitz.open()
    for text in pages_content:
        page = doc.new_page()
        page.insert_text((72, 100), text, fontsize=12)
    doc.save(path)
    doc.close()
    return path


class TestAnchorMultiPageEnforcement:
    def test_page_0_rule_extracts_from_page_0(self, tmp_path):
        pdf = make_pdf(tmp_path, ["Date: 2024-01-01", "Date: 2024-06-01"])
        rule = AnchorExtractionRule(
            key_name="date", data_type="STRING",
            anchor_text="Date:", page_index=0
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        assert result is not None
        assert "2024-01-01" in result

    def test_page_1_rule_returns_none_when_called_with_page_0(self, tmp_path):
        pdf = make_pdf(tmp_path, ["Date: 2024-01-01", "Date: 2024-06-01"])
        rule = AnchorExtractionRule(
            key_name="date", data_type="STRING",
            anchor_text="Date:", page_index=1
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)  # Called with page 0, but rule says page 1
        doc.close()
        assert result is None

    def test_page_1_rule_extracts_from_page_1(self, tmp_path):
        pdf = make_pdf(tmp_path, ["Invoice: INV-001", "Invoice: INV-002"])
        rule = AnchorExtractionRule(
            key_name="inv", data_type="STRING",
            anchor_text="Invoice:", page_index=1
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 1)
        doc.close()
        assert result is not None
        assert "INV-002" in result


class TestAnchorMatchIndex:
    def _make_repeated_pdf(self, tmp_path) -> str:
        """Create PDF with 3 'Label:' anchors on same page."""
        path = str(tmp_path / "repeated.pdf")
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Label: first_value", fontsize=11)
        page.insert_text((72, 100), "Label: second_value", fontsize=11)
        page.insert_text((72, 128), "Label: third_value", fontsize=11)
        doc.save(path)
        doc.close()
        return path

    def test_match_index_0_picks_first(self, tmp_path):
        pdf = self._make_repeated_pdf(tmp_path)
        rule = AnchorExtractionRule(
            key_name="v", data_type="STRING",
            anchor_text="Label:", match_index=0, page_index=0
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        assert result is not None
        assert "first" in result.lower()

    def test_match_index_exceeds_count_returns_none(self, tmp_path):
        pdf = self._make_repeated_pdf(tmp_path)
        rule = AnchorExtractionRule(
            key_name="v", data_type="STRING",
            anchor_text="Label:", match_index=99, page_index=0
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        assert result is None


class TestAnchorSearchModes:
    def test_case_insensitive_match(self, tmp_path):
        pdf = make_pdf(tmp_path, ["TOTAL: 500"])
        rule = AnchorExtractionRule(
            key_name="total", data_type="STRING",
            anchor_text="total:", search_mode=SearchMode.CASE_INSENSITIVE,
            page_index=0
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(pdf)
        result = strategy.extract(doc, 0)
        doc.close()
        assert result is not None
        assert "500" in result

    def test_regex_mode(self, tmp_path):
        """Test regex anchor mode finds the anchor and returns a non-null result."""
        path = str(tmp_path / "regex_test.pdf")
        doc = fitz.open()
        page = doc.new_page()
        # Write anchor on the left and value on the right with clear separation
        page.insert_text((72, 100), "Ref-001:", fontsize=12)
        page.insert_text((200, 100), "ABCXYZ", fontsize=12)
        doc.save(path)
        doc.close()

        rule = AnchorExtractionRule(
            key_name="item", data_type="STRING",
            anchor_text=r"Ref-\d+:", search_mode=SearchMode.REGEX,
            page_index=0
        )
        strategy = AnchorExtractionStrategy(rule)
        doc = fitz.open(path)
        result = strategy.extract(doc, 0)
        doc.close()
        assert result is not None
        assert "ABCXYZ" in result
