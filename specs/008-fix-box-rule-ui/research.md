# Research Phase

## NEEDS CLARIFICATION: Coordinate Mapping
- **Issue**: PyMuPDF (`fitz`) uses `page.rect` for text extraction coordinates, which represents the CropBox. The CropBox does not always start at `(0, 0)`.
- **Current Behavior**: The `bounding_box_strategy` calculates `x0 = pct * page.rect.width`. It ignores `page.rect.x0`. If `page.rect.x0` is not zero, the extracted region will be shifted relative to what was visually selected.
- **Decision**: Update `PdfService` to provide the full `page.rect` (including `x0, y0`), and update the strategies (`bounding_box_strategy.py` and `anchor_strategy.py`) to add the `x0` and `y0` offset. `x0 = page.rect.x0 + pct * width`.

## Implementation Approach for Reselecting Region
- **Decision**: Add a "Reselect Region" button to the rule list or Rule Dialog. However, since selecting a region requires interacting with the `WorkspaceTabWidget` canvas, it is better to handle it in `WorkspaceTabWidget` when a user wants to edit the rule's region.
- **Alternatives**: 
  1. Have a button in `RuleDialog`. If clicked, hide the dialog, let user draw, then re-show.
  2. Have a dedicated mode in the main UI for editing a selected rule.
- **Chosen Alternative**: Option 1 is standard in PyQt for modal dialogs. We can add a "Reselect Region" button in `RuleDialog`. When clicked, it `accept()`s with a special code or triggers a signal to the controller to enter "reselect" mode for that rule. But `RuleDialog` already takes `predefined_box`.
Actually, if the user edits the rule, they can't change the box.
If we change the `RuleDialog` to have a button `[Reselect Box on Canvas]`, when clicked, we can close the dialog with a special return code (e.g. `2`), wait for the user to select the box on the canvas, and then re-open the dialog.
OR, easier: just add a button in `WorkspaceTabWidget` near "Edit Rule": "Reselect Region". When clicked, enter selection mode. When selection completes, update the `box` property of the currently selected rule without showing the full dialog, or show the dialog with the new box.

## Implementation Approach for Rule Deletion
- **Decision**: Add a "Delete Rule" button to the `WorkspaceTabWidget` UI. When clicked, prompt the user for confirmation. If confirmed, remove the rule from `template.rules` and the UI table.
