# Implementation Plan: Advanced Preview

**Branch**: `003-advanced-preview` | **Date**: 2026-09-19 | **Spec**: [spec.md](file:///d:/Coding/LearnSpecKit/Proj1/specs/003-advanced-preview/spec.md)

**Input**: Feature specification from `/specs/003-advanced-preview/spec.md`

## Summary

This feature replaces the basic message box preview with a comprehensive spreadsheet-like interface (`QTableWidget`) for viewing full extractions and exporting them to CSV. It also introduces a per-rule preview button directly within the main rules table to allow fast, isolated testing of individual extraction rules.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: PySide6, PyMuPDF, Pydantic

**Storage**: None (CSV export is transient file writing)

**Testing**: `pytest`, `pytest-qt`

**Target Platform**: Windows / macOS / Linux

**Project Type**: Desktop Application

**Performance Goals**: UI should remain responsive while previewing rules.

**Constraints**: CSV exports must handle large string blocks properly (using standard `csv` module).

**Scale/Scope**: Moderate UI updates. Touches the existing `WorkspaceTabWidget`, `TemplateController`, and creates two new dialogs (`PreviewDialog` and `RulePreviewDialog`).

## Constitution Check

*GATE: Passed*

- **I. Desktop-First Architecture**: Changes leverage PySide6 `QTableWidget` and `QDialog` to provide a robust desktop UI.
- **II. Test-Driven Quality**: The new dialogs rely entirely on existing, tested extraction strategies.
- **III. Simple and Extensible Extraction Rules**: No changes to the underlying extraction models are necessary.

## Project Structure

### Documentation (this feature)

```text
specs/003-advanced-preview/
├── plan.md              
├── research.md          
├── data-model.md        
└── quickstart.md        
```

### Source Code (repository root)

```text
src/
├── controllers/
│   └── template_controller.py (orchestrates preview dialogs and extraction)
└── ui/
    ├── workspace_tab.py (adds Actions column and preview buttons)
    ├── preview_dialog.py (new tabular CSV export dialog)
    └── rule_preview_dialog.py (new single-rule text dialog)
```

**Structure Decision**: Extending the existing desktop app layout. All modifications are strictly within the `ui` and `controllers` layers.
