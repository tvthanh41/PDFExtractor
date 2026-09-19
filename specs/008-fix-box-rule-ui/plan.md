# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Fix the UI for managing extraction rules by allowing users to reselect bounding box regions and delete rules. Additionally, fix coordinate mapping between PyQt6 and PyMuPDF to account for page offsets (CropBox).

## Technical Context

**Language/Version**: Python 3.11

**Primary Dependencies**: PySide6, PyMuPDF (fitz)

**Storage**: Local files (.pdftpl JSON)

**Testing**: pytest

**Target Platform**: Desktop (Windows, macOS, Linux)

**Project Type**: Desktop Application

**Performance Goals**: UI remains responsive.

**Constraints**: N/A

**Scale/Scope**: Small desktop application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Desktop-First Architecture**: Changes are confined to PySide6 UI and PDF services, maintaining responsiveness.
- [x] **Test-Driven Quality**: Core logic changes in `PdfService` and strategies need tests.
- [x] **Simple and Extensible Extraction Rules**: No changes to the underlying model, ensuring backwards compatibility.
- [x] **Decoupled Logic**: Coordinate mapping fixes are applied to the extraction strategies, keeping UI logic separate from parsing logic.

## Project Structure

### Documentation (this feature)

```text
specs/008-fix-box-rule-ui/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
src/
├── controllers/
│   └── template_controller.py
├── services/
│   └── pdf_service.py
├── strategies/
│   ├── anchor_strategy.py
│   └── bounding_box_strategy.py
└── ui/
    └── workspace_tab.py
```

**Structure Decision**: Single Python project structure. Changes will be localized to existing files in the MVC architecture.
