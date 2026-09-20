# Research & Decisions: Multi-Page Navigation and Pattern-Based Table Detection

## 1. Multi-Page Navigation in PySide6 Canvas

- **Decision**: Extend `PdfCanvasWidget` to manage page state (`current_page`, `total_pages`) and expose page switching signals. Add dedicated navigation toolbar controls (`btn_prev`, `spin_page`, `lbl_total`, `btn_next`) to `WorkspaceTab`.
- **Rationale**: PyMuPDF's `fitz.Document` already provides random access to any page (`doc.load_page(n)` or `doc[n]`). The current implementation only loaded page 0 upon document opening. Exposing page navigation in the UI canvas allows users to view and interact with all pages smoothly without blocking the UI thread.
- **Alternatives Considered**:
  - Continuous vertical scroll rendering all pages simultaneously in a single `QGraphicsScene`: Adds significant memory overhead and complexity with bounding box coordinate transformations across page boundaries. Page-by-page navigation with pagination controls is cleaner, faster, and standard in PDF extraction tools.
  - Page thumbnails sidebar: Helpful for visual browsing, but page spinbox + next/prev buttons deliver immediate MVP value with minimal UI clutter and zero performance overhead.

---

## 2. Dynamic Table Boundary Detection & Decoupled Architecture

- **Decision**: Create a dedicated, headless `BoundaryDetector` service (`src/services/boundary_detector.py`) that calculates dynamic bounding boxes using `PatternBoundaryConfig` (`start_pattern`, `end_pattern`, `include_start`, `include_end`, `is_regex`, `skip_k`).
- **Rationale**: Keeps `TableExtractionStrategy` clean and avoids spaghetti code. The boundary detector isolates regex and string matching, line coordinate calculations, and occurrence filtering (`skip_k`), making it 100% unit-testable without requiring PySide6 UI components or Qt event loops.
- **Alternatives Considered**:
  - Inlining boundary detection directly in `TableExtractionStrategy`: Creates bloated, tightly coupled strategy code that is difficult to maintain and test.
  - Performing pattern search on the client/GUI side: Violates Constitution Principle "Decoupled Architecture" because headless batch runs would not be able to compute dynamic table boundaries.

---

## 3. Anchor & Pattern Occurrence Selection (`skip_k`)

- **Decision**: Explicitly support occurrence filtering by standardizing `skip_k` (skipping the first $k$ matches and picking the $(k+1)$-th match).
- **Rationale**: Real-world documents (e.g. multi-section invoices or financial reports) frequently contain repeated tokens (such as "Subtotal:", "Total:", or "Date:"). Standardizing `skip_k: int = 0` (0 = first match, 1 = skip 1st and pick 2nd) allows both `AnchorExtractionRule` and `PatternBoundaryConfig` to handle duplicate matches deterministically.
- **Alternatives Considered**:
  - Negative indexing (e.g. -1 for last match): Can be ambiguous when total match count varies across batch documents. Skip $k$ provides an intuitive, forward-scanning selection.

---

## 4. PyMuPDF4LLM Integration

- **Decision**: Add `pymupdf4llm>=0.0.17` to `requirements.txt`. Extend `TableConfig` with an `engine` selector (`TableEngine.PYMUPDF` vs `TableEngine.PYMUPDF4LLM`). When PyMuPDF4LLM is selected, parse markdown table structures into normalized `List[List[str]]` or key-value dictionaries.
- **Rationale**: `pymupdf4llm` leverages heuristics specifically optimized for layout analysis and markdown table reconstruction. Normalizing its output to `List[List[str]]` preserves 100% compatibility with existing `CSVExporter`, `PreviewDialog`, and table rule preview workflows.
- **Alternatives Considered**:
  - Outputting raw markdown string into the table result: Incompatible with downstream tabular data processing and CSV structured export.
  - Separate `PyMuPDF4LLMStrategy` class: Less cohesive for users who think of table extraction as a single task with selectable engine backends. However, strategy factory can delegate internally to a layout extractor engine cleanly.

---

## 5. Page Index Propagation Across All Rule Types

- **Decision**: Add `page_index: int = 0` to `AnchorExtractionRule` (which previously lacked it) and ensure `TemplateController.preview_extraction()`, `TemplateController.test_rule_extraction()`, and `BatchEngine.process_file_worker()` always pass `rule.page_index` to strategy execution.
- **Rationale**: Eliminates the current bug where preview extraction and anchor extraction hardcode page 0 or the current canvas view page, causing multi-page rule evaluation to fail.
- **Alternatives Considered**:
  - Multi-page search (search all pages until found): Unpredictable performance on 100+ page documents and can match unintended text on irrelevant pages. Explicit `page_index` ensures deterministic rule execution.
