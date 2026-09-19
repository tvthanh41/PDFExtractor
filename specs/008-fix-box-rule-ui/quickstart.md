# Quickstart & Validation Guide

## 1. Validating Coordinate Mapping
1. Launch the application: `python src/main.py`.
2. Create a new template and load a PDF file that has a non-zero CropBox offset (e.g. cropped in a PDF editor).
3. Select "New Rule", choose a region on the canvas, and save it as a bounding box rule.
4. Click on the rule in the rule list to preview extraction.
5. **Expected Outcome**: The extracted text should exactly match the text inside the drawn red rectangle, regardless of the PDF's internal CropBox settings.

## 2. Validating Rule Deletion
1. Launch the application and add a dummy rule.
2. Select the dummy rule from the rule list.
3. Click the "Delete Rule" button.
4. Confirm the deletion in the popup dialog.
5. **Expected Outcome**: The rule disappears from the list, the preview clears, and the highlight on the canvas disappears.

## 3. Validating Rule Reselection
1. Create a box rule with a specific region.
2. Select the rule in the list.
3. Click "Reselect Region".
4. The cursor will change to crosshairs. Draw a new region on the canvas.
5. **Expected Outcome**: The rule's coordinates are immediately updated. Clicking the rule again highlights the *new* region, and the extraction preview updates to reflect the text in the new region.
