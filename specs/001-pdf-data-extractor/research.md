# Phase 0 Research: PDF Data Extractor Architecture & Technology Selection

**Feature**: PDF Data Extractor  
**Date**: 2026-09-18  

## Technology Stack Decisions

### 1. Programming Language & Standards
- **Decision**: Python 3.11+ using standard PEP 8 coding conventions, `typing` annotations, and `pydantic` v2 for data validation.
- **Rationale**: Python provides rich ecosystem libraries for PDF parsing, multi-threading/processing, and cross-platform desktop UI development.
- **Alternatives Considered**: C# / .NET (Windows-centric), C++ (over-complex for text extraction domain).

### 2. GUI Framework Selection
- **Decision**: `PySide6` (Qt 6 for Python).
- **Rationale**:
  - High DPI awareness with auto-scaling to screen resolutions (utilizing `QScreen.availableGeometry()`).
  - Advanced `QGraphicsView`/`QGraphicsScene` canvas capabilities allowing zoom, pan, and interactive drag-and-drop bounding box selection over rendered PDF pages.
  - Native multi-tab container (`QTabWidget`) for managing multiple template workspaces simultaneously.
  - Robust thread safety via Qt Signals and Slots for async progress updates during batch processing.
- **Alternatives Considered**:
  - `CustomTkinter`: Good look, but lacks advanced vector/graphics canvas primitives needed for multi-page PDF rendering and bounding box manipulators.
  - `PyQt6`: Similar functionality, but dual GPL licensing makes PySide6 (LGPL) preferable.

### 3. PDF Parsing & Rendering Engine
- **Decision**: `PyMuPDF` (`fitz`).
- **Rationale**:
  - Extremely fast C-backed PDF parsing and rasterization (up to 10x faster than pure Python parsers).
  - Provides exact bounding box coordinates (`x0, y0, x1, y1`) for extracted text and block-level layout analysis.
  - High quality render to `QImage` for display in the interactive UI editor.
- **Alternatives Considered**:
  - `pdfplumber`: Built on `pdfminer.six`, accurate but significantly slower for batch processing large document sets (1000+ files).
  - `pypdf`: Fast text extraction but lacks rich rendering and word-level spatial positioning capabilities needed for anchor-offset extraction.

### 4. Architecture & Design Patterns
- **Decision**: Clean Layered Architecture (Domain, Application, Infrastructure, UI) with design patterns:
  - **Strategy Pattern**: `IExtractionStrategy` interface with `AnchorExtractionStrategy` and `BoundingBoxExtractionStrategy`. Extensible for future `OCRExtractionStrategy` (scanned PDFs).
  - **Observer Pattern**: Qt Signals/Slots to decouple long-running batch extraction from UI responsiveness.
  - **Factory Pattern**: `ExtractionStrategyFactory` to build rule engines from template definitions.
  - **Repository Pattern**: `TemplateRepository` to handle template serialization/deserialization.
- **Rationale**: Ensures complete decoupling between extraction algorithms, storage, and GUI representation.
- **OCR Extension Strategy**: Scanned document support can be added later by creating an `OcrExtractionStrategy` implementing `IExtractionStrategy` without altering the batch execution engine or UI flow.

### 5. Multi-Core Parallel Execution Engine
- **Decision**: `concurrent.futures.ProcessPoolExecutor` with batch chunking.
- **Rationale**: Utilizing process pools bypasses Python GIL bottlenecks, enabling full utilization of all CPU cores when parsing thousands of PDF documents.
- **Alternatives Considered**: `ThreadPoolExecutor` (limited by Python GIL during heavy regex and coordinate math processing).

### 6. Template Storage & CSV Output Formats
- **Decision**:
  - Template File: JSON schema saved with `.pdftpl` extension.
  - Export Format: Standard UTF-8 CSV with `csv.DictWriter` and double-quote escaping.
- **Rationale**: JSON is human-readable, schema-validatable, and portable. CSV is universal for tabular data consumers (Excel, Pandas, Databases).
