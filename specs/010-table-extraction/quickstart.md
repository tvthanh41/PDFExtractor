# Quickstart & Validation Guide: Table Extraction

This guide describes how to validate the Table Extraction feature end-to-end once implemented.

## Prerequisites

- Python 3.11+
- Virtual environment created and activated
- Dependencies installed: `pip install -r requirements.txt`

## 1. Unit Tests Verification

Run pytest on the new unit test suites:

```bash
pytest tests/unit/test_table_rule.py tests/unit/test_table_strategy.py tests/unit/test_csv_exporter_table.py -v
```

**Expected Outcome**: All unit tests pass, confirming rule serialization, PyMuPDF strategy extraction, and JSON formatting in CSV export.

## 2. Integration & Batch Processing Test

Run the batch extraction integration test:

```bash
pytest tests/integration/test_batch_table_extraction.py -v
```

**Expected Outcome**: Batch engine processes sample PDF with a table rule, extracts structured 2D array, and exports to CSV with valid JSON payload in the rule's column.

## 3. UI Manual Verification

1. Launch the application:
   ```bash
   python -m src.main
   ```
2. Open a sample PDF containing a table.
3. Click **Add Rule** and select **Table** as the rule type.
4. Draw a bounding box around the table on the PDF canvas.
5. In the rule configuration dialog:
   - Toggle **Has Borders** off/on.
   - Adjust **Vertical Strategy** to `text` or `lines`.
   - Set **Header Rows Count** to `1`.
6. Click **Preview** or **Save Rule**.
7. Run **Batch Process** and inspect the output CSV file: verify the table column contains JSON-serialized rows and columns matching the PDF table.
