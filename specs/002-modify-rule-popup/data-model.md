# Phase 1: Data Model & State

This feature does not require changes to the persistent Pydantic data models (`AnchorExtractionRule`, `BoundingBoxExtractionRule`, `Template`).

The changes are entirely transient UI state.

## Transient UI State

### `TemplateController`
- **New State**: `selected_rule_id: Optional[str] = None`
  - **Purpose**: Tracks which rule is currently selected in the UI so that the canvas can highlight its bounding box and the preview panel can display its extracted result.

### `WorkspaceTabWidget`
- **UI Element**: `QTableWidget` (Rule list)
  - **Change**: `setEditTriggers(QAbstractItemView.NoEditTriggers)` applied during initialization.
  - **New Signal**: Emits a custom signal or directly calls controller methods when a row is selected or double-clicked.

### `RuleDialog`
- **Constructor Input**: `rule: Optional[ExtractionRule] = None`
  - **State**: If `rule` is provided, the dialog operates in "Edit Mode". The `rule_id` is preserved. When `get_rule()` is called, it returns a new rule instance with the same `rule_id` but updated properties, which the controller then uses to replace the existing rule in the template's rule list.
