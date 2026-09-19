# Quickstart: Advanced Preview

This guide explains how to validate the Advanced Preview features end-to-end.

## Prerequisites
1. Ensure dependencies are installed: `uv sync`
2. Start the application: `uv run python src/main.py`
3. Load a PDF (e.g. `sample/scorereport.pdf`) using the **Open PDF** button.
4. Add at least two rules (e.g., an Anchor rule for "Passing Score:" and a Bounding Box rule).

## Validation Scenario 1: Tabular Preview and CSV Export
1. Click the **Preview Extraction** button in the top toolbar.
2. **Verify**: A new `PreviewDialog` window opens.
3. **Verify**: The table contains columns matching your rule keys, and the extracted data is populated in the first row.
4. **Action**: Drag the column headers to ensure they resize.
5. **Action**: Click the **Export to CSV** button and save the file to your desktop.
6. **Verify**: Open the CSV file and confirm the data matches the table.

## Validation Scenario 2: Per-Rule Preview
1. Look at the rules data table on the right panel.
2. **Verify**: There is an **Actions** column with a **Preview** button for each rule.
3. **Action**: Click the **Preview** button for the Anchor rule.
4. **Verify**: A new `RulePreviewDialog` opens specifically showing the text for that single rule.
5. **Verify**: The text area can be scrolled and resized if the text is large.
