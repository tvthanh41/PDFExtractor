"""
BoundaryDetector — Headless service for dynamic table boundary detection.

Scans a fitz.Page for start/end text patterns, applies skip_k occurrence
selection, and returns a fitz.Rect representing the detected table region.

For multi-page documents, use :meth:`BoundaryDetector.detect_bounds_in_doc`
which accepts a start_page_index and scans forward until a match is found.
This module is completely decoupled from PySide6/UI components.
"""
from __future__ import annotations

import re
from typing import Optional

import pymupdf as fitz

from src.domain.models import PatternBoundaryConfig


class BoundaryDetector:
    """
    Headless service that locates a table's bounding rectangle on a page
    by searching for start and end text patterns.

    Usage (single page)::

        from src.services.boundary_detector import BoundaryDetector

        rect = BoundaryDetector.detect_bounds(page, config)
        if rect:
            table_data = page.find_tables(clip=rect)

    Usage (multi-page — start scanning from a given page)::

        result = BoundaryDetector.detect_bounds_in_doc(doc, config, start_page_index=1)
        if result:
            found_page, rect = result
            table_data = doc[found_page].find_tables(clip=rect)
    """

    @staticmethod
    def detect_bounds(
        page: fitz.Page,
        config: PatternBoundaryConfig,
    ) -> Optional[fitz.Rect]:
        """
        Locate the vertical extent of a table on *page* using *config*.

        The method:
        1. Searches all text spans on the page for matches to ``start_pattern``
           and ``end_pattern`` (literal or regex, case-sensitive).
        2. Applies ``skip_k``: skips the first *k* ``start_pattern`` matches
           and picks the *(k+1)*-th match as the anchor.
        3. After selecting the start anchor, scans **downward** from that
           position for the first occurrence of ``end_pattern``.
        4. Adjusts y-coordinates based on ``include_start`` / ``include_end``.
        5. Returns a ``fitz.Rect`` spanning the full page width (x0=0, x1=page.rect.width)
           with the computed y0/y1 bounds, or ``None`` if any anchor is not found.

        Args:
            page:   The ``fitz.Page`` to scan.
            config: A ``PatternBoundaryConfig`` describing the patterns and
                    boundary-inclusion preferences.

        Returns:
            ``fitz.Rect`` or ``None``.
        """
        start_matches = BoundaryDetector._find_pattern_matches(page, config.start_pattern, config.is_regex)
        if len(start_matches) <= config.skip_k:
            return None  # Not enough occurrences after applying skip_k

        # Select the (skip_k + 1)-th match as the start anchor
        start_match = start_matches[config.skip_k]
        start_rect: fitz.Rect = start_match["rect"]

        # Search for end_pattern **below** the chosen start anchor
        end_matches = BoundaryDetector._find_pattern_matches(
            page, config.end_pattern, config.is_regex, below_y=start_rect.y1
        )
        if not end_matches:
            return None
        end_match = end_matches[0]
        end_rect: fitz.Rect = end_match["rect"]

        # Apply include/exclude for start
        if config.include_start:
            y0 = start_rect.y0
        else:
            y0 = start_rect.y1  # top of region starts just BELOW the start pattern line

        # Apply include/exclude for end
        if config.include_end:
            y1 = end_rect.y1
        else:
            y1 = end_rect.y0  # bottom of region ends just ABOVE the end pattern line

        if y0 >= y1:
            return None  # Degenerate rectangle

        page_width = page.rect.width
        return fitz.Rect(0, y0, page_width, y1)

    @staticmethod
    def detect_bounds_in_doc(
        doc: fitz.Document,
        config: "PatternBoundaryConfig",
        start_page_index: int = 0,
    ) -> "Optional[tuple[int, fitz.Rect]]":
        """
        Scan pages of *doc* starting at *start_page_index* and return the
        first page where the pattern boundaries are successfully matched.

        This implements the "page_index as start page" behaviour for pattern
        matching: we begin at ``start_page_index`` and work forward, returning
        as soon as we find a page that has both the start and end patterns.

        Args:
            doc:              The open ``fitz.Document`` to scan.
            config:           A ``PatternBoundaryConfig`` describing the patterns.
            start_page_index: The first page to inspect (0-based, inclusive).

        Returns:
            ``(page_number, fitz.Rect)`` for the first matching page, or
            ``None`` if no page matched.
        """
        start_page_index = max(0, start_page_index)
        for page_num in range(start_page_index, len(doc)):
            rect = BoundaryDetector.detect_bounds(doc[page_num], config)
            if rect is not None:
                return (page_num, rect)
        return None

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _find_pattern_matches(
        page: fitz.Page,
        pattern: str,
        is_regex: bool,
        below_y: Optional[float] = None,
    ) -> list[dict]:
        """
        Return all text-block matches for *pattern* on *page*, sorted top-to-bottom.

        Args:
            page:     The page to search.
            pattern:  A literal or regex string.
            is_regex: Whether *pattern* is a regular expression.
            below_y:  If given, only return matches whose top edge (y0) is
                      **at or below** this y-coordinate.

        Returns:
            List of dicts with keys ``"text"`` and ``"rect"`` (``fitz.Rect``).
        """
        matches: list[dict] = []

        # Extract word-level bounding boxes for precise line positions
        words = page.get_text("words")  # list of (x0, y0, x1, y1, word, block_no, line_no, word_no)

        # Group words into lines (same block_no + line_no)
        from collections import defaultdict
        line_map: dict[tuple, list] = defaultdict(list)
        for w in words:
            key = (w[5], w[6])  # (block_no, line_no)
            line_map[key].append(w)

        for key in sorted(line_map):
            line_words = sorted(line_map[key], key=lambda w: w[0])  # sort by x0
            line_text = " ".join(w[4] for w in line_words)
            # Bounding rect for the whole line
            x0 = min(w[0] for w in line_words)
            y0 = min(w[1] for w in line_words)
            x1 = max(w[2] for w in line_words)
            y1 = max(w[3] for w in line_words)
            line_rect = fitz.Rect(x0, y0, x1, y1)

            if below_y is not None and y0 < below_y:
                continue  # Skip lines above the anchor

            matched = (
                bool(re.search(pattern, line_text))
                if is_regex
                else pattern in line_text
            )
            if matched:
                matches.append({"text": line_text, "rect": line_rect})

        return matches
