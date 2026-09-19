# Implementation Plan: PDF Data Extractor

**Branch**: `001-pdf-data-extractor` | **Date**: 2026-09-18 | **Spec**: [spec.md](file:///d:/Coding/LearnSpecKit/Proj1/specs/001-pdf-data-extractor/spec.md)

**Input**: Feature specification from `/specs/001-pdf-data-extractor/spec.md`

## Summary

Build a high-performance desktop application in Python for extracting structured data from PDF documents using reusable templates. The application features a modern, resolution-responsive PySide6 multi-tab UI allowing users to visually define extraction rules via Anchor Search (text key + direction offset + data type) or visual Bounding Box selection. Templates are saved in JSON format (`.pdftpl`). The batch processing engine filters input directories to select only `.pdf` files, executes extraction concurrently using multi-core process pools, and exports formatted records into CSV files. The architecture enforces Clean Code principles and the Strategy Pattern (`IExtractionStrategy`), ensuring seamless future extensibility for scanned document OCR processing.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: PySide6 (Qt 6 GUI framework), PyMuPDF (`fitz` PDF rendering & spatial text parsing engine), Pydantic v2 (data validation & JSON schema serialization).

**Storage**: File-based storage (JSON schema for `.pdftpl` templates, standard UTF-8 for `.csv` output files).

**Testing**: `pytest`, `pytest-qt` for UI component testing, `pytest-cov`.

**Target Platform**: Windows / macOS / Linux Desktop.

**Project Type**: Desktop GUI Application.

**Performance Goals**: Process 100 single-page PDF files in under 15 seconds using multi-core parallel worker pools. UI responsiveness maintained at >=30 FPS during batch runs.

**Constraints**:
- **Resolution Responsiveness**: Window sizing and widget layout MUST be dynamically computed relative to display resolution (`QScreen.availableGeometry()`). Zero hardcoded window dimensions.
- **Scanned Document Extensibility**: Extraction algorithms MUST be encapsulated behind an `IExtractionStrategy` interface so OCR support for scanned documents can be added without modifying UI or engine logic.
- **Clean Code & Conventions**: PEP 8 compliance, explicit type hint annotations, clean separation of concerns (Domain, Application Services, Strategy, UI Views, Controllers).

**Scale/Scope**: ~15 source modules in single project layout.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Rule 1: Modular / Decoupled Design**: PASSED. Business domain & strategy logic isolated from PySide6 UI views.
- **Rule 2: Automated Testing**: PASSED. Unit tests for strategy parsers, schema validators, CSV builders, and integration tests for process pools.
- **Rule 3: Observability & Error Handling**: PASSED. Batch execution logs errors per PDF file into execution logs without halting execution.

## Project Structure

### Documentation (this feature)

```text
specs/001-pdf-data-extractor/
├── spec.md              # Feature Specification
├── plan.md              # Implementation Plan (this document)
├── research.md          # Phase 0 Research & Technology Choices
├── data-model.md        # Phase 1 Data Model & Entity Specifications
├── quickstart.md        # Phase 1 Quickstart & Manual/Automated Test Scenarios
└── contracts/           # Phase 1 Interface Contracts
    ├── template-schema.json
    ├── csv-export-contract.md
    └── gui-architecture-contract.md
```

### Source Code Layout

```text
src/
├── main.py                     # Application entry point (PySide6 QApplication setup)
├── config.py                   # Global configuration & app constants
├── domain/                     # Core Domain Layer (Pure Python)
│   ├── models.py               # Pydantic domain models (Template, Rule, BoundingBox, Job)
│   └── enums.py                # Enums (DataType, SearchMode, Direction, RuleType)
├── strategies/                 # Strategy Pattern Engine
│   ├── base.py                 # Abstract IExtractionStrategy interface
│   ├── anchor_strategy.py      # Anchor search & spatial offset parser
│   ├── bounding_box_strategy.py # Bounding box percentage coordinate parser
│   └── factory.py              # ExtractionStrategyFactory
├── services/                   # Application Services
│   ├── pdf_service.py          # PyMuPDF document rendering & text block extraction
│   ├── batch_engine.py         # Parallel ProcessPoolExecutor batch runner
│   ├── template_repository.py  # JSON file persistence (.pdftpl)
│   └── csv_exporter.py         # Structured CSV builder
├── ui/                         # Presentation Layer (PySide6 Views)
│   ├── main_window.py          # Resolution-responsive QMainWindow with QTabWidget
│   ├── workspace_tab.py        # Template tab workspace (canvas + rule list)
│   ├── pdf_canvas.py           # QGraphicsView canvas (PDF render + bounding box drag tool)
│   ├── rule_dialog.py          # Dialog to define Anchor / Bounding Box rules
│   └── batch_dialog.py         # Batch execution progress & log dialog
└── controllers/                # Presenters / Controllers
    ├── template_controller.py  # Template tab state controller
    └── batch_controller.py     # Async batch execution runner & signal bridge

tests/
├── unit/                       # Unit tests for strategies, models, and CSV exporter
│   ├── test_anchor_strategy.py
│   ├── test_bounding_box_strategy.py
│   └── test_template_repository.py
├── integration/                # Integration tests for PyMuPDF & ProcessPool batch engine
│   └── test_batch_engine.py
└── ui/                         # PySide6 UI tests
    └── test_main_window.py
```

**Structure Decision**: Single project layout with clean layer separation (`domain`, `strategies`, `services`, `ui`, `controllers`).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No constitution violations. Architecture adheres to clean code standards and standard design patterns.*
