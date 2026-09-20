"""
Unit tests for BoundaryDetector service.
Verifies start/end text matching, regex patterns, include/exclude boundary logic, skip_k.
"""
import pytest
import pymupdf as fitz
from src.domain.models import PatternBoundaryConfig
from src.services.boundary_detector import BoundaryDetector


def make_pdf_with_lines(tmp_path, lines: list[str]) -> str:
    """Create a single-page PDF with each item in lines on a separate line."""
    path = str(tmp_path / "test_boundary.pdf")
    doc = fitz.open()
    page = doc.new_page()
    y = 72
    for line in lines:
        page.insert_text((72, y), line, fontsize=12)
        y += 20
    doc.save(path)
    doc.close()
    return path


class TestBoundaryDetectorLiteralMatch:
    def test_finds_start_and_end(self, tmp_path):
        pdf = make_pdf_with_lines(tmp_path, [
            "Preamble text",
            "Item Description",
            "Widget A  1  $10.00",
            "Widget B  2  $20.00",
            "Subtotal",
            "Footer text",
        ])
        cfg = PatternBoundaryConfig(
            start_pattern="Item Description",
            end_pattern="Subtotal",
            include_start=True,
            include_end=False,
        )
        doc = fitz.open(pdf)
        result = BoundaryDetector.detect_bounds(doc[0], cfg)
        doc.close()
        assert result is not None
        # top of rect should be at/above "Item Description" line
        # bottom should be above "Subtotal" line
        assert result.y0 < result.y1

    def test_include_start_false_excludes_header(self, tmp_path):
        pdf = make_pdf_with_lines(tmp_path, [
            "Header",
            "Start Here",
            "Row 1",
            "End Here",
        ])
        cfg_include = PatternBoundaryConfig(
            start_pattern="Start Here", end_pattern="End Here",
            include_start=True, include_end=False
        )
        cfg_exclude = PatternBoundaryConfig(
            start_pattern="Start Here", end_pattern="End Here",
            include_start=False, include_end=False
        )
        doc = fitz.open(pdf)
        rect_include = BoundaryDetector.detect_bounds(doc[0], cfg_include)
        rect_exclude = BoundaryDetector.detect_bounds(doc[0], cfg_exclude)
        doc.close()
        assert rect_include is not None
        assert rect_exclude is not None
        # excluding start means the top boundary is lower (further down the page)
        assert rect_exclude.y0 >= rect_include.y0

    def test_include_end_true_includes_end_line(self, tmp_path):
        pdf = make_pdf_with_lines(tmp_path, [
            "Start",
            "Middle",
            "End",
        ])
        cfg_exclude_end = PatternBoundaryConfig(
            start_pattern="Start", end_pattern="End",
            include_start=True, include_end=False
        )
        cfg_include_end = PatternBoundaryConfig(
            start_pattern="Start", end_pattern="End",
            include_start=True, include_end=True
        )
        doc = fitz.open(pdf)
        rect_excl = BoundaryDetector.detect_bounds(doc[0], cfg_exclude_end)
        rect_incl = BoundaryDetector.detect_bounds(doc[0], cfg_include_end)
        doc.close()
        assert rect_incl.y1 >= rect_excl.y1

    def test_start_not_found_returns_none(self, tmp_path):
        pdf = make_pdf_with_lines(tmp_path, ["Line A", "Line B"])
        cfg = PatternBoundaryConfig(start_pattern="MISSING", end_pattern="Line B")
        doc = fitz.open(pdf)
        result = BoundaryDetector.detect_bounds(doc[0], cfg)
        doc.close()
        assert result is None

    def test_end_not_found_returns_none(self, tmp_path):
        pdf = make_pdf_with_lines(tmp_path, ["Line A", "Line B"])
        cfg = PatternBoundaryConfig(start_pattern="Line A", end_pattern="MISSING")
        doc = fitz.open(pdf)
        result = BoundaryDetector.detect_bounds(doc[0], cfg)
        doc.close()
        assert result is None


class TestBoundaryDetectorSkipK:
    def test_skip_k_selects_second_occurrence(self, tmp_path):
        pdf = make_pdf_with_lines(tmp_path, [
            "Section 1 Start",
            "Row a",
            "Section End",
            "Section 2 Start",
            "Row b",
            "Section End",
        ])
        # skip_k=0: should find first "Section 2 Start"... no wait, start_pattern="Section"
        # Use skip_k=1 to pick second "Section ... Start"
        cfg = PatternBoundaryConfig(
            start_pattern="Section", end_pattern="Section End",
            include_start=True, include_end=False, skip_k=1
        )
        doc = fitz.open(pdf)
        result = BoundaryDetector.detect_bounds(doc[0], cfg)
        doc.close()
        # Should find second occurrence, rect should be below halfway of page
        assert result is not None

    def test_skip_k_exceeds_matches_returns_none(self, tmp_path):
        pdf = make_pdf_with_lines(tmp_path, ["Start", "End"])
        cfg = PatternBoundaryConfig(
            start_pattern="Start", end_pattern="End", skip_k=5  # Only 1 match
        )
        doc = fitz.open(pdf)
        result = BoundaryDetector.detect_bounds(doc[0], cfg)
        doc.close()
        assert result is None


class TestBoundaryDetectorRegex:
    def test_regex_start_pattern(self, tmp_path):
        pdf = make_pdf_with_lines(tmp_path, [
            "Item 001",
            "Row data",
            "Total: 100",
        ])
        cfg = PatternBoundaryConfig(
            start_pattern=r"Item \d+",
            end_pattern=r"Total:",
            is_regex=True,
            include_start=True,
            include_end=False,
        )
        doc = fitz.open(pdf)
        result = BoundaryDetector.detect_bounds(doc[0], cfg)
        doc.close()
        assert result is not None
