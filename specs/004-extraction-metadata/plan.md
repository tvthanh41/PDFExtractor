# Implementation Plan: Extraction Metadata

**Branch**: `004-extraction-metadata` | **Date**: 2026-09-19 | **Spec**: [spec.md](file:///d:/Coding/LearnSpecKit/Proj1/specs/004-extraction-metadata/spec.md)

**Input**: Feature specification from `/specs/004-extraction-metadata/spec.md`

## Summary

This feature automatically injects predefined system metadata (File Name, File Path, Generated Time, User, Template Name) into all extraction outputs, including the Batch CSV exporter and the Preview UI. This avoids cluttering the user's template rules with system-level context.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Standard library (`os`, `getpass`, `datetime`)

**Storage**: Transacted at output time (CSV / Dict)

**Testing**: `pytest`

**Target Platform**: Windows / macOS / Linux

**Project Type**: Desktop Application

**Performance Goals**: Negligible impact (<10ms).

**Constraints**: `getpass.getuser()` can throw exceptions in certain headless environments; requires a safe fallback.

**Scale/Scope**: Minor code injection. Touches `TemplateController` (for preview) and `CSVExporter` (for batch exports).

## Constitution Check

*GATE: Passed*

- **I. Desktop-First Architecture**: Fits seamlessly into existing PySide6 components.
- **II. Test-Driven Quality**: We will test `CSVExporter`'s new headers and `TemplateController`'s preview dict construction.
- **III. Simple and Extensible Extraction Rules**: Preserves `.pdftpl` purity by handling metadata strictly at the edge layer.

## Project Structure

### Documentation (this feature)

```text
specs/004-extraction-metadata/
├── plan.md              
├── research.md          
├── data-model.md        
└── quickstart.md        
```

### Source Code (repository root)

```text
src/
├── controllers/
│   └── template_controller.py (Add metadata to preview results)
└── services/
    └── csv_exporter.py (Add metadata columns to batch export)
```

**Structure Decision**: Modifications remain contained within the extraction edge layers (export/preview).
