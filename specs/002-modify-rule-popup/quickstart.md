# Quickstart Validation Guide

Follow these steps to manually validate the "Modify Rule via Popup GUI" feature once implemented.

## Prerequisites
- The application must be running: `python src/main.py`
- A sample PDF loaded into the workspace.

## Scenario 1: Inline Editing Disabled
1. Add a new rule (either Anchor or Bounding Box).
2. The rule appears in the table.
3. Double-click or type into any cell in the rule's row.
4. **Expected Outcome**: The cell does not enter edit mode. No text cursor appears.

## Scenario 2: Edit Rule via Popup
1. Double-click the rule row in the table (or use an Edit button if implemented).
2. **Expected Outcome**: The `RuleDialog` opens.
3. Verify that the dialog fields (Key Name, Data Type, etc.) are pre-populated with the rule's current values.
4. Change the "Key Name" to a new value (e.g., `updated_key`) and click "Save".
5. **Expected Outcome**: The dialog closes and the table updates to show `updated_key`. No new row is added (the list count remains the same).

## Scenario 3: Canvas Highlighting & Preview
1. Add a Bounding Box rule and define a box on the canvas.
2. Ensure no rule is selected in the table. The box should appear in its default style (e.g., blue outline).
3. Click the rule in the table to select it.
4. **Expected Outcome**: The bounding box on the canvas changes its visual style (e.g., thick red border with semi-transparent fill) to indicate selection.
5. A popup or dedicated panel shows the preview of the extracted data for that rule.
6. Click empty space in the table to deselect the rule.
7. **Expected Outcome**: The bounding box returns to its default unselected style, and the preview clears.
