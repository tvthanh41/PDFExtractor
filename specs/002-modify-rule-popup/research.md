# Phase 0: Outline & Research

## Research Tasks

1. **How to disable inline editing in PySide6 `QTableWidget`?**
   - **Decision**: Set the table's edit triggers to `QAbstractItemView.NoEditTriggers`.
   - **Rationale**: This is the standard Qt way to make a table read-only while still allowing row selection.
   - **Alternatives considered**: Subclassing `QItemDelegate`, but that is overly complex for simply disabling edits globally on the table.

2. **How to pass an existing rule to `RuleDialog` for editing?**
   - **Decision**: Update the `RuleDialog.__init__` signature to accept an optional `rule: ExtractionRule = None` argument. If provided, the UI fields (Key Name, Data Type, Rule Type, etc.) are pre-populated from the rule's properties, and the "Save" action updates the existing rule object (or returns a modified copy).
   - **Rationale**: Reusing the same dialog for both creation and modification keeps the UI consistent and reduces code duplication.

3. **How to highlight a bounding box on the PDF canvas?**
   - **Decision**: The `TemplateController` will maintain a `selected_rule_id`. When a rule is selected in the table, the controller updates this ID and triggers a canvas repaint. The canvas rendering logic will draw the selected bounding box with a distinct color (e.g., solid red with a semi-transparent fill) compared to unselected boxes (e.g., blue outline).
   - **Rationale**: Retained mode GUI state driven by the controller ensures the canvas always reflects the true selection state without tight coupling to the table widget itself.

4. **How to trigger the rule modification?**
   - **Decision**: Connect the `doubleClicked` signal of the rule table to an `edit_rule` slot in the `TemplateController`. Alternatively, add an "Edit" button next to the "Add Rule" button. For now, double-clicking a row is the most intuitive approach for desktop applications.
   - **Rationale**: Matches standard desktop UX expectations.
