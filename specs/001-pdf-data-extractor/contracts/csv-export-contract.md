# Contract: CSV Export Format

**Feature**: PDF Data Extractor  
**Date**: 2026-09-18  

## Format Specification

1. **Encoding**: UTF-8 with optional BOM for Microsoft Excel compatibility.
2. **Line Endings**: Standard CRLF (`\r\n`) or LF (`\n`).
3. **Delimiter**: Comma (`,`).
4. **Quoting Rule**: All text values containing commas, double quotes (`"`), or newlines MUST be enclosed in double quotes. Double quotes inside values MUST be escaped as `""`.
5. **Fixed Metadata Columns**:
   - `_file_name`: Original PDF filename (e.g. `invoice_1001.pdf`).
   - `_file_path`: Full or relative path to target PDF file.
   - `_status`: Execution status (`SUCCESS`, `PARTIAL_SUCCESS`, `FAILED`).
6. **Template Key Columns**:
   - Arranged in exact order matching `Template.rules`.
   - Column header matches `rule.key_name`.

## Example Output Structure

```csv
_file_name,_file_path,_status,vendor_name,total_amount,invoice_date
"invoice_001.pdf","C:/data/invoice_001.pdf","SUCCESS","ACME Corp",1250.50,"2026-09-18"
"statement_99.pdf","C:/data/statement_99.pdf","PARTIAL_SUCCESS","Bank of Asia",,"2026-09-01"
```
