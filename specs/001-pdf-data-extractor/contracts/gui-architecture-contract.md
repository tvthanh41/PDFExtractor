# Contract: GUI Architecture & Design Patterns

**Feature**: PDF Data Extractor  
**Date**: 2026-09-18  

## UI Design & Resolution Handling Guidelines

1. **No Hardcoded Screen Dimensions**:
   - The main application window MUST initialize dynamically based on target system screen resolution:
     ```python
     screen = QApplication.primaryScreen().availableGeometry()
     window_width = int(screen.width() * 0.8)
     window_height = int(screen.height() * 0.8)
     main_window.resize(window_width, window_height)
     ```
   - All layouts must use PySide6 `QVBoxLayout`, `QHBoxLayout`, `QGridLayout`, and `QSplitter` with stretch factors, ensuring smooth resizing on displays ranging from 1080p to 4K.

2. **Clean MVC / MVP Architecture**:
   - **View (`ui/`)**: Displays widgets, handles PySide6 canvas events, captures bounding box rubber-band selections, emits Qt Signals.
   - **Presenter/Controller (`controllers/`)**: Handles UI actions, bridges domain services, triggers background worker threads.
   - **Model (`domain/`)**: Pure Python Pydantic dataclasses and extraction business logic (independent of PySide6/Qt).

3. **Multi-Tab Document Workspace**:
   - `QTabWidget` root container where each tab represents an active `TemplateWorkspaceWidget`.
   - Each workspace tab manages its own sample PDF preview canvas, rule editor table, and unsaved state flag.

4. **Extensibility for OCR & Custom Engines (Strategy Pattern)**:
   - Extraction engine delegates to `IExtractionStrategy` abstract base interface.
   - Current implementation: `PdfiumTextStrategy` (digital text PDF parsing).
   - Future extension point: `TesseractOcrStrategy` (scanned PDF image text recognition) implements `IExtractionStrategy` without requiring UI or engine refactoring.
