from __future__ import annotations

from typing import Optional, List, Dict, Any, Union
import pymupdf as fitz

from src.strategies.base import IExtractionStrategy
from src.domain.models import TableExtractionRule
from src.domain.enums import TableBoundaryType, TableEngine
from src.services.pdf_service import PdfService


class TableExtractionStrategy(IExtractionStrategy):
    """
    Strategy for extracting structured tabular data from a PDF page.

    Supports two boundary modes:
    - BOUNDING_BOX: Uses a static, user-defined percentage-based clip rect.
    - PATTERN_MATCH: Dynamically detects the table region using BoundaryDetector.

    Supports two extraction engines:
    - PYMUPDF (default): Uses page.find_tables() from PyMuPDF.
    - PYMUPDF4LLM: Uses pymupdf4llm.to_markdown() with markdown table parsing.
    """

    def __init__(self, rule: TableExtractionRule):
        self.rule = rule

    def extract(
        self, doc: fitz.Document, page_num: int
    ) -> Optional[Union[List[List[str]], Dict[str, str]]]:
        boundary_type = getattr(self.rule, 'boundary_type', TableBoundaryType.BOUNDING_BOX)

        if boundary_type == TableBoundaryType.PATTERN_MATCH:
            # Pattern mode: page_index is the *start* page.  We scan forward
            # from rule.page_index and extract on the first matching page.
            # The outer loop calls extract() for every page; only act when
            # we are on page_num == rule.page_index (the trigger page) so
            # that we don't run the expensive scan on every single page.
            if page_num != self.rule.page_index:
                return None
            return self._extract_pattern_mode(doc)
        else:
            # BOUNDING_BOX mode: exact page match required.
            if page_num != self.rule.page_index:
                return None
            if page_num < 0 or page_num >= len(doc):
                return None
            page = doc[page_num]
            target_rect = self._resolve_target_rect_bbox(doc, page, page_num)
            if target_rect is None:
                return {} if getattr(self.rule.config, 'extract_as_key_value', False) else []
            return self._run_engine(page, target_rect)

    # ------------------------------------------------------------------
    # Pattern-mode multi-page extraction
    # ------------------------------------------------------------------

    def _extract_pattern_mode(
        self, doc: fitz.Document
    ) -> Optional[Union[List[List[str]], Dict[str, str]]]:
        """Scan forward from rule.page_index; extract on the first matching page."""
        if not self.rule.pattern_boundary:
            return {} if getattr(self.rule.config, 'extract_as_key_value', False) else []
        from src.services.boundary_detector import BoundaryDetector
        result = BoundaryDetector.detect_bounds_in_doc(
            doc, self.rule.pattern_boundary, start_page_index=self.rule.page_index
        )
        if result is None:
            return {} if getattr(self.rule.config, 'extract_as_key_value', False) else []
        found_page_num, target_rect = result
        page = doc[found_page_num]
        return self._run_engine(page, target_rect)

    def _run_engine(
        self, page: fitz.Page, target_rect: fitz.Rect
    ) -> Union[List[List[str]], Dict[str, str]]:
        """Dispatch to the configured extraction engine."""
        engine = getattr(self.rule.config, 'engine', TableEngine.PYMUPDF)
        if engine == TableEngine.PYMUPDF4LLM:
            return self._extract_via_pymupdf4llm(page, target_rect)
        return self._extract_via_pymupdf(page, target_rect)

    # ------------------------------------------------------------------
    # Boundary resolution (bounding box mode)
    # ------------------------------------------------------------------

    def _resolve_target_rect_bbox(
        self, doc: fitz.Document, page: fitz.Page, page_num: int
    ) -> Optional[fitz.Rect]:
        """Return the clip Rect for BOUNDING_BOX boundary type."""
        if not self.rule.box:
            return None
        page_x0, page_y0, width, height = PdfService.get_page_dimensions(doc, page_num)
        x0 = page_x0 + self.rule.box.x_pct * width
        y0 = page_y0 + self.rule.box.y_pct * height
        x1 = x0 + (self.rule.box.width_pct * width)
        y1 = y0 + (self.rule.box.height_pct * height)
        return fitz.Rect(x0, y0, x1, y1)

    # ------------------------------------------------------------------
    # PyMuPDF native extraction
    # ------------------------------------------------------------------

    def _extract_via_pymupdf(
        self, page: fitz.Page, target_rect: fitz.Rect
    ) -> Union[List[List[str]], Dict[str, str]]:
        strategy_kwargs = {
            "clip": target_rect,
            "snap_tolerance": self.rule.config.snap_tolerance,
        }

        if self.rule.config.has_borders:
            strategy_kwargs["strategy"] = "lines"
        else:
            strategy_kwargs["strategy"] = "text"

        if hasattr(self.rule.config, 'vertical_strategy') and self.rule.config.vertical_strategy:
            strategy_kwargs["vertical_strategy"] = self.rule.config.vertical_strategy.value
        if hasattr(self.rule.config, 'horizontal_strategy') and self.rule.config.horizontal_strategy:
            strategy_kwargs["horizontal_strategy"] = self.rule.config.horizontal_strategy.value

        try:
            tabs = page.find_tables(**strategy_kwargs)
        except Exception:
            tabs = page.find_tables(clip=target_rect)

        if not tabs or not tabs.tables:
            try:
                tabs = page.find_tables(clip=target_rect)
            except Exception:
                tabs = None

        if tabs and tabs.tables:
            raw_data = tabs.tables[0].extract()
            return self._post_process(raw_data)

        return {} if getattr(self.rule.config, 'extract_as_key_value', False) else []

    # ------------------------------------------------------------------
    # PyMuPDF4LLM extraction (layout-aware markdown path)
    # ------------------------------------------------------------------

    def _extract_via_pymupdf4llm(
        self, page: fitz.Page, target_rect: fitz.Rect
    ) -> Union[List[List[str]], Dict[str, str]]:
        """
        Use pymupdf4llm.to_markdown to extract layout-aware text within the
        clip region, then parse any markdown table(s) found in the output.
        Falls back to native PyMuPDF extraction if an error occurs.
        """
        try:
            import pymupdf4llm
            # to_markdown accepts clip as a fitz.Rect
            md_text: str = pymupdf4llm.to_markdown(
                page.parent,  # fitz.Document
                pages=[page.number],
                clip=target_rect,
            )
            rows = _parse_markdown_table(md_text)
            if rows:
                return self._post_process(rows)
            # No markdown table found — fall back to native
        except Exception:
            pass

        return self._extract_via_pymupdf(page, target_rect)

    # ------------------------------------------------------------------
    # Shared post-processing
    # ------------------------------------------------------------------

    def _post_process(
        self, raw_data: List[List[Any]]
    ) -> Union[List[List[str]], Dict[str, str]]:
        """Clean cell values and optionally convert to key-value dict."""
        cleaned_table = []
        for row in raw_data:
            cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
            cleaned_table.append(cleaned_row)

        if getattr(self.rule.config, 'extract_as_key_value', False):
            kv_dict: Dict[str, str] = {}
            for row in cleaned_table:
                if not row:
                    continue
                key = row[0]
                if not key:
                    continue
                if len(row) == 2:
                    val = row[1]
                elif len(row) > 2:
                    val = " ".join(c for c in row[1:] if c)
                else:
                    val = ""
                kv_dict[key] = val
            return kv_dict

        return cleaned_table


# ---------------------------------------------------------------------------
# Markdown table parser (used by pymupdf4llm path)
# ---------------------------------------------------------------------------

def _parse_markdown_table(markdown_text: str) -> List[List[str]]:
    """
    Parse the first markdown table found in *markdown_text* into a list of rows.

    Each row is a ``List[str]`` of cell values.  The separator row (``|---|``)
    is skipped.  Returns an empty list if no table is found.

    Example input::

        | Name   | Qty | Price |
        |--------|-----|-------|
        | Widget |  1  | $10   |

    Returns::

        [["Name", "Qty", "Price"], ["Widget", "1", "$10"]]
    """
    import re as _re

    rows: List[List[str]] = []
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # Skip separator rows like |---|---|
        if _re.match(r"^\|[\s\-:]+(\|[\s\-:]+)*\|?$", stripped):
            continue
        # Parse cells
        cells = [cell.strip() for cell in stripped.split("|")]
        # Remove empty strings from leading/trailing pipe
        cells = [c for c in cells if c != "" or len(cells) > 2]
        cells = cells[1:-1] if cells and cells[0] == "" else cells
        if cells:
            rows.append(cells)
    return rows
