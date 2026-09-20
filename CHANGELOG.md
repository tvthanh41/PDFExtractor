# Changelog

All notable changes to **PDF Data Extractor** will be documented in this file.

This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions
and uses [Semantic Versioning](https://semver.org/).

> **For contributors**: Every user-visible change (feature, fix, removal) MUST be recorded under
> `## [Unreleased]` before the work is considered complete. When a version is released, promote
> the `[Unreleased]` section to a dated version heading and add a fresh `[Unreleased]` block above.

---

## [Unreleased]

_(No unreleased changes yet.)_

---

## [1.1.0] - 2026-09-20

### Added

- **Table rule — Pattern-Based Boundary Detection** (`BoundaryDetector` service): Users can now
  define a table extraction rule using a **start pattern** and an **end pattern** instead of a
  static bounding box. The detector dynamically locates the table region at extraction time,
  making rules robust against variable-length tables (e.g. invoices with different numbers of line
  items). Options include:
  - Include/exclude the start line in the extracted region.
  - Include/exclude the end line in the extracted region.
  - Regex mode — patterns are treated as Python regular expressions when enabled.
  - `skip_k` — skip the first *k* occurrences of the start pattern and use the *(k+1)*-th match,
    useful when the same header text appears multiple times on a page.
- **Multi-page PDF navigation**: The workspace canvas now renders all pages of a loaded document.
  Users can navigate via Prev/Next buttons or by typing a page number directly. The total page
  count is displayed beside the navigation spinner.
- **Page-aware extraction rules**: Every rule type (Anchor, Bounding Box, Table) now stores a
  `page_index` field. Rules default to the page that was active when they were created. Batch
  extraction respects each rule's own page index, enabling templates that pull data from different
  pages of the same document.
- **PyMuPDF4LLM extraction engine**: A second table extraction engine (`PyMuPDF4LLM`) is now
  available as an advanced option alongside the native PyMuPDF engine. It uses layout-aware
  Markdown parsing, which can improve accuracy on borderless or complex tables.
- **Anchor `skip_k` parameter**: Anchor-text search rules can now skip the first *k* matches and
  use the next one, giving precise control over which occurrence of a label is used as the anchor.
- **`TableExtractionRule` Pydantic model** with `TableBoundaryType` enum (`BOUNDING_BOX` /
  `PATTERN_MATCH`) and `PatternBoundaryConfig` sub-model.
- **`TableStrategy` class** — unified strategy that handles both bounding-box and pattern-match
  boundary modes, and delegates to either the PyMuPDF or PyMuPDF4LLM engine.
- **Vietnamese locale (`vi.json`)** fully populated with all UI strings and tooltips.
- **Table rule in `RuleDialog`**: Advanced configuration panel for table rules, including boundary
  mode toggle, pattern inputs, engine selector, has-borders toggle, extract-as-key-value toggle,
  vertical/horizontal strategy combos, header-row count, and snap tolerance.
- **Excel-like table preview** (`RulePreviewDialog`): Clicking the per-rule **Preview** button for
  a table rule now displays results in a `QTableWidget` grid with frozen column headers and
  alternating row colours instead of raw monospace text. Dict results use a two-column key/value
  grid. Scalar values fall back to a plain text view.
- **Fix — Preview button did nothing**: The per-rule Preview button in the rules list was looking
  up the wrong column index (`3` instead of `4`), so it never fired. Fixed.
- **Comprehensive test suite for new features** (50+ new test files / cases):
  - `test_boundary_detector.py` — literal match, include/exclude start & end, `skip_k`, regex.
  - `test_multipage_models.py` — `PatternBoundaryConfig`, `TableExtractionRule`, page index fields.
  - `test_pattern_table_strategy.py` — strategy extraction with pattern boundaries.
  - `test_table_strategy.py` / `test_table_advanced_strategy.py` — PyMuPDF engine, key-value mode,
    `RulePreviewDialog` rendering.
  - `test_pymupdf4llm_table_strategy.py` — PyMuPDF4LLM engine branch.
  - `test_multipage_canvas.py` — page navigation signals and canvas rendering.
  - `test_anchor_strategy_multipage.py` — page-aware anchor extraction.
  - `test_page_index_execution.py` — batch engine respects per-rule `page_index`.
  - `test_multipage_batch.py` (integration) — full multipage batch extraction pipeline.
  - `test_batch_table_extraction.py` (integration) — batch extraction with table rules.
  - `test_csv_exporter_table.py` — table data serialised as JSON string in CSV column.

---

## [1.0.0] - 2026-09-19

Initial public release of **PDF Data Extractor**.

### Added

- **Visual Template Editor**: PySide6 desktop application with a zoomable PDF canvas. Users draw
  bounding boxes or configure anchor rules interactively on the document.
- **Multi-tab workspace**: Open and work on multiple extraction templates simultaneously, each in
  its own tab. Each tab is independently saveable.
- **Extraction rule types**:
  - **Anchor Search** — locate a label text on the page, then extract a value at a configurable
    offset and direction (right, left, above, below). Supports literal and substring search modes,
    configurable `match_index`, and `offset_distance`.
  - **Bounding Box** — extract all text within a percentage-coordinate region drawn on the canvas.
    Coordinates are stored as fractions of the page dimensions, making them resolution-independent.
- **Rule Dialog** with advanced panel (collapsed by default) for offset distance, match index,
  page index, and extraction direction.
- **Live single-rule preview**: Click **Preview** next to any rule to instantly see the extracted
  value from the currently loaded document.
- **Full extraction preview**: The **Preview Extraction** toolbar button runs all rules and
  displays results in a scrollable `QTableWidget` with one column per rule key.
- **Template persistence**: Templates are serialised to/from `.pdftpl` files (JSON via Pydantic).
  Load an existing template to restore all rules and configuration.
- **Batch processing**: Run a template against an entire directory of PDF files (recursive).
  Processing is parallelised across CPU cores. Results are written to a CSV file with one row per
  PDF file.
- **Batch configuration dialog**: Select template path, input directory, output CSV path, and
  worker count before starting a batch job. A progress dialog shows live status.
- **CSV export**: All extracted keys become column headers; each PDF becomes one data row. Table
  results are serialised to a compact JSON string in their column so the CSV remains flat.
- **Extraction metadata columns** automatically prepended to every CSV row: `file name`,
  `file path`, `generated time`, `user`, `template name`.
- **Internationalisation (i18n)** via a locale JSON loader. English (`en.json`) locale ships by
  default; locale can be switched from Settings without restarting.
- **Settings dialog**: Select UI language. Preference is persisted between sessions.
- **Tooltips** on every interactive control, sourced from the active locale file.
- **Standalone executable build** (`build_app.py` / PyInstaller): Produces a single-file
  `PDFExtractor.exe` with bundled locales and icon (`resources/app_icon.ico`).
- **Automated test suite** (pytest + pytest-qt):
  - Unit: `test_strategies.py`, `test_models.py`, `test_i18n.py`, `test_rule_dialog_advanced.py`.
  - Integration: `test_batch_engine.py`, `test_batch_config.py`, `test_real_pdf_extraction.py`.

### Dependencies

| Package | Role |
|---|---|
| `PySide6` | GUI framework (Qt bindings) |
| `pymupdf` | PDF rendering and text extraction |
| `pymupdf4llm` | Layout-aware Markdown extraction engine |
| `pydantic` | Rule/template data models and validation |
| `pyinstaller` | Standalone executable packaging |
| `pytest` / `pytest-qt` | Testing framework |

---

[Unreleased]: https://github.com/tvthanh41/Proj1/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/tvthanh41/Proj1/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/tvthanh41/Proj1/releases/tag/v1.0.0
