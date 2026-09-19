# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Fixes the issue where loaded templates default to "New Template" in the UI and extraction outputs by enforcing the filename as the template name upon load/save. Also introduces a `BatchConfigDialog` to confirm batch job paths before starting execution, preventing accidental runs.

## Technical Context

**Language/Version**: Python 3.x

**Primary Dependencies**: PySide6, PyMuPDF

**Storage**: Local file system (JSON serialized into `.pdftpl`)

**Testing**: `pytest`

**Target Platform**: Desktop (Windows/macOS/Linux)

**Project Type**: Desktop UI Application

**Performance Goals**: N/A (UI prompt)

**Constraints**: Must not block main thread unnecessarily, but dialog is modal.

**Scale/Scope**: Local usage, a few files.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Architecture aligns with Desktop-First (PySide6 dialog used).
- [x] Test-driven quality (will write tests for dialog integration and name extraction).
- [x] Simple and Extensible rules (Data model untouched).

## Project Structure

### Documentation (this feature)

```text
specs/005-featurename-005-batch-config/
├── plan.md
├── research.md
├── data-model.md
└── quickstart.md
```

### Source Code

```text
src/
├── controllers/
│   ├── template_controller.py
│   └── app_controller.py (implicit)
├── services/
│   └── template_repository.py
└── ui/
    └── batch_config_dialog.py [NEW]

tests/
└── integration/
    └── test_batch_config.py [NEW]
```

**Structure Decision**: A new UI component `batch_config_dialog.py` will be created in `src/ui/`. The logic to update names will reside in `template_repository.py` and `template_controller.py`.
