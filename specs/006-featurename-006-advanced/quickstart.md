# Quickstart: Advanced Rule Configuration

## Validation Scenario 1: Anchor Rule — Offset Distance & Match Index

1. Open the application and load a PDF.
2. Click **Add Rule** → choose **Anchor Search**.
3. Fill in Key Name = `date`, Anchor Text = `Date:`, Direction = `RIGHT`.
4. Click **▶ Advanced Settings** to expand the section.
5. **Verify**: `Offset Distance` shows `150.0` and `Match Index` shows `0` (defaults).
6. Change `Offset Distance` to `300.0` and `Match Index` to `1`.
7. Click **Save**.
8. Click **Edit** on the rule just created.
9. Click **▶ Advanced Settings**.
10. **Verify**: `Offset Distance` = `300.0` and `Match Index` = `1` (persisted correctly).

## Validation Scenario 2: Bounding Box Rule — Page Index

1. Draw a bounding box on the canvas.
2. In the Rule Dialog that appears, fill Key Name = `summary`.
3. Click **▶ Advanced Settings**.
4. **Verify**: `Page Index` shows `0` (default).
5. Change `Page Index` to `2`.
6. Click **Save**.
7. Click **Edit** on the rule.
8. Click **▶ Advanced Settings**.
9. **Verify**: `Page Index` = `2`.
10. Open the saved `.pdftpl` file in a text editor and **verify**: `"page_index": 2`.

## Validation Scenario 3: Default workflow unchanged

1. Create an Anchor rule **without** opening Advanced Settings.
2. Save the template and inspect the `.pdftpl` file.
3. **Verify**: `"offset_distance": 150.0` and `"match_index": 0` are present (defaults applied).
