# Implementation Plan: Modify Rule via Popup GUI

**Branch**: `002-modify-rule-popup` | **Date**: 2026-09-19 | **Spec**: [spec.md](file:///D:/Coding/LearnSpecKit/Proj1/specs/002-modify-rule-popup/spec.md)

**Input**: Feature specification from `/specs/002-modify-rule-popup/spec.md`

## Summary

This feature replaces the inline table editing of extraction rules with a dedicated popup GUI (`RuleDialog`), allowing for complex rule configurations without UI clutter. Additionally, selecting a rule from the list will display its extracted data preview and highlight its bounding box on the PDF canvas for visual verification.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: PySide6, PyMuPDF, Pydantic

**Storage**: JSON `.pdftpl` files (existing)

**Testing**: `pytest`, `pytest-qt`

**Target Platform**: Windows / macOS / Linux

**Project Type**: Desktop Application

**Performance Goals**: UI updates and canvas highlighting must occur within 500ms of rule selection.

**Constraints**: Logic must remain decoupled from the UI layer to support headless batch processing.

**Scale/Scope**: Moderate UI updates. Touches the existing `RuleDialog`, `WorkspaceTabWidget`, and `TemplateController`.

## Constitution Check

*GATE: Passed*

- **I. Desktop-First Architecture**: Changes are purely UI-focused and maintain responsiveness.
- **II. Test-Driven Quality**: UI changes will need `pytest-qt` tests to verify dialog population and table read-only state.
- **III. Simple and Extensible Extraction Rules**: No changes to the underlying Pydantic models are required; only transient UI state is added.

## Project Structure

### Documentation (this feature)

```text
specs/002-modify-rule-popup/
├── plan.md              
├── research.md          
├── data-model.md        
└── quickstart.md        
```

### Source Code (repository root)

```text
src/
├── controllers/
│   └── template_controller.py (handle rule selection logic)
└── ui/
    ├── rule_dialog.py (add edit mode, pre-populate fields)
    ├── workspace_tab.py (disable inline editing, add selection signal)
    └── pdf_canvas.py (support highlighted bounding box rendering)

tests/
└── ui/
    └── test_rule_dialog.py (add tests for edit mode)
```

**Structure Decision**: We are extending the existing single-project desktop app layout. All modifications are within the `ui` and `controllers` layers.
