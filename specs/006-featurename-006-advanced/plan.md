# Implementation Plan: Advanced Rule Configuration

**Branch**: `006-advanced-rule-config` | **Date**: 2026-09-19 | **Spec**: specs/006-featurename-006-advanced/spec.md

## Summary

Exposes three hidden rule configuration fields in the Rule Dialog UI via a collapsible "Advanced Settings" section. No domain model changes are needed — all fields already exist in `AnchorExtractionRule` and `BoundingBoxExtractionRule` with correct defaults. The only changes are in the UI dialog and the `_create_rule` / `_populate` methods.

## Technical Context

**Language/Version**: Python 3.x

**Primary Dependencies**: PySide6

**Storage**: N/A (existing `.pdftpl` JSON format already serializes these fields)

**Testing**: `pytest`

**Target Platform**: Desktop (Windows/macOS/Linux)

**Project Type**: Desktop UI Application

**Performance Goals**: N/A

**Constraints**: Dialog must resize cleanly when Advanced Settings is toggled.

## Constitution Check

- [x] Desktop-First: Pure PySide6 UI change.
- [x] Test-Driven: Unit/integration tests will cover round-trip serialization of advanced values.
- [x] Simple and Extensible: No new fields or abstraction layers; existing model fields are wired up.

## Project Structure

### Documentation

```text
specs/006-featurename-006-advanced/
├── plan.md
├── research.md
├── data-model.md
└── quickstart.md
```

### Source Code

```text
src/
└── ui/
    └── rule_dialog.py          [MODIFY — add advanced sections + update _create_rule + _populate]

tests/
└── unit/
    └── test_rule_dialog_advanced.py  [NEW — unit tests for advanced field round-trip]
```

**Structure Decision**: Single-file UI change. No new files except for the test.

## Proposed Changes

### `src/ui/rule_dialog.py` [MODIFY]

1. In the **Anchor** stacked page: after `direction_combo`, add:
   - A `QPushButton("▶ Advanced Settings")` (toggle)
   - A hidden `QGroupBox` containing:
     - `QDoubleSpinBox` for `offset_distance` (min=0, max=9999, step=10.0, default=150.0)
     - `QSpinBox` for `match_index` (min=0, max=99, default=0)

2. In the **Bounding Box** stacked page: after the info label, add:
   - A `QPushButton("▶ Advanced Settings")` (toggle)
   - A hidden `QGroupBox` containing:
     - `QSpinBox` for `page_index` (min=0, max=999, default=0)

3. Update `_populate(rule)` to pre-fill advanced fields when editing.

4. Update `_create_rule()` to read advanced fields instead of using hardcoded defaults.

## Verification Plan

### Automated Tests
```
uv run pytest tests/unit/test_rule_dialog_advanced.py -v
uv run pytest tests/ -v
```

### Manual Verification
- Follow all 3 scenarios in `quickstart.md`.
