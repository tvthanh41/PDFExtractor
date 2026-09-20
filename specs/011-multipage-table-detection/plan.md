# Implementation Plan: Multi-Page Navigation and Pattern-Based Table Detection

**Branch**: `011-multipage-table-detection` | **Date**: 2026-09-19 | **Spec**: [spec.md](file:///d:/Coding/LearnSpecKit/Proj1/specs/011-multipage-table-detection/spec.md)

**Input**: Feature specification from `specs/011-multipage-table-detection/spec.md`

## Summary

This feature expands the PDF Data Extractor application to provide seamless multi-page document navigation in the PySide6 viewer, page-indexed rule execution across all strategies, dynamic pattern-based table boundary detection (`start_pattern`, `end_pattern`, `include_start`, `include_end`, `skip_k`), repeated anchor occurrence selection (`skip_k`), and enhanced layout-aware table extraction using `pymupdf4llm`. The architecture cleanly decouples boundary coordinate detection into a headless service (`BoundaryDetector`), ensuring robust headless batch execution and high testability without architectural regression.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: PySide6 (UI), PyMuPDF (PDF rendering & native table detection), pymupdf4llm (layout-aware markdown table reconstruction), Pydantic v2 (domain validation & JSON serialization)
**Storage**: JSON/pdftpl template files, CSV export files
**Testing**: pytest, pytest-qt
**Target Platform**: Desktop (Windows x64 / cross-platform PySide6)
**Project Type**: Desktop GUI Application with Headless Batch Processor
**Performance Goals**: Page transitions rendered in < 500ms; table pattern boundary detection executed in < 100ms per page
**Constraints**: Zero UI coupling in data parsing / strategy layers; backward compatibility with existing saved templates
**Scale/Scope**: Supports multi-page documents (1 to 1,000+ pages) in single-file and batch modes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Principle I (Desktop-First Architecture)**: PySide6 canvas page transitions are fast; heavy extraction runs headlessly; batch processing operates on worker threads.
- [x] **Principle II (Test-Driven Quality)**: Unit tests planned for `BoundaryDetector`, `AnchorExtractionRule`, `TableExtractionRule`, and `TableExtractionStrategy`.
- [x] **Principle III (Simple and Extensible Extraction Rules)**: `TableExtractionRule` and `AnchorExtractionRule` extended using clean Pydantic fields with backward-compatible defaults.
- [x] **Additional Constraints (Decoupled Parsing Logic)**: `BoundaryDetector` and extraction strategies take raw `fitz.Page` and `fitz.Document` without importing PySide6 widgets.
- [x] **Development Workflow**: `requirements.txt` updated to include `pymupdf4llm`.

## Project Structure

### Documentation (this feature)

```text
specs/011-multipage-table-detection/
├── plan.md              # This implementation plan
├── research.md          # Phase 0 architectural decisions
├── data-model.md        # Phase 1 domain models & enums
├── quickstart.md        # Phase 1 validation walkthrough
├── contracts/           # Phase 1 JSON schema contracts
│   └── pattern-table-rule-schema.json
└── tasks.md             # Phase 2 output (/speckit-tasks command)
```

### Source Code Layout

```text
src/
├── domain/
│   ├── enums.py              # Added TableBoundaryType, TableEngine
│   └── models.py             # PatternBoundaryConfig, updated TableExtractionRule & AnchorExtractionRule
├── services/
│   ├── boundary_detector.py  # NEW: Headless pattern-based table boundary detection
│   ├── batch_engine.py       # Updated: Page-index propagation across all rules
│   └── template_repository.py
├── strategies/
│   ├── base.py
│   ├── anchor_strategy.py    # Updated: Page-index and occurrence skip handling
│   ├── table_strategy.py     # Updated: Dynamic boundary detection & PyMuPDF4LLM engine
│   └── factory.py
├── ui/
│   ├── pdf_canvas.py         # Updated: Multi-page navigation (next/prev/set_page)
│   ├── workspace_tab.py      # Updated: Navigation toolbar controls (buttons, spinbox, total)
│   └── rule_dialog.py        # Updated: Page index field, Pattern table boundary controls, engine selection
└── controllers/
    └── template_controller.py# Updated: Page navigation hooks & page-aware rule test/preview

tests/
├── unit/
│   ├── test_boundary_detector.py  # NEW: Unit tests for pattern matching & coordinate computation
│   ├── test_multipage_canvas.py   # NEW: Tests for canvas page navigation
│   └── test_table_strategy.py     # Updated: Tests for pattern boundaries & PyMuPDF4LLM
└── integration/
    └── test_multipage_batch.py    # NEW: Multi-page batch extraction tests
```

**Structure Decision**: Single desktop application architecture with clean layered separation (domain models, headless services, extraction strategies, UI canvas/dialogs, controllers).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| None | N/A | N/A - Adheres strictly to existing design principles without introducing unnecessary layers or dependencies. |
