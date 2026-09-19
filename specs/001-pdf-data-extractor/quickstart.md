# Quickstart Validation Guide: PDF Data Extractor

**Feature**: PDF Data Extractor  
**Date**: 2026-09-18  

## Setup & Environment Verification

### Prerequisites
- Python 3.10+
- Virtual environment (`venv`)

### Installation Commands
```bash
# Create and activate virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install PySide6 PyMuPDF pydantic pytest
```

---

## Validation Scenario 1: Launch GUI & Dynamic Scaling Test

1. Launch application:
   ```bash
   python -m src.main
   ```
2. **Expected Outcome**:
   - Application launches smoothly filling ~80% of current display screen resolution.
   - Multi-tab template workspace is visible with a "Welcome / New Template" tab.
   - Resizing window scales all panels, preview canvas, and rule list proportionally.

---

## Validation Scenario 2: Create Template & Define Rules

1. Click "Open Sample PDF" and select a sample invoice PDF.
2. Define Anchor Rule:
   - Search Text: `"Tổng giá trị"`
   - Direction: `RIGHT`
   - Data Type: `CURRENCY`
   - Key Name: `total_amount`
3. Define Bounding Box Rule:
   - Drag rubber-band selection over header address block.
   - Key Name: `vendor_address`
4. Save template as `sample_bank_fee.pdftpl`.
5. **Expected Outcome**:
   - Preview canvas highlights matched anchor value and bounding box region.
   - `sample_bank_fee.pdftpl` is created on disk following valid [template JSON schema](file:///d:/Coding/LearnSpecKit/Proj1/specs/001-pdf-data-extractor/contracts/template-schema.json).

---

## Validation Scenario 3: Batch Extraction & Parallel Output Verification

1. In GUI (or via CLI validation runner), select `sample_bank_fee.pdftpl` and target directory containing 50 PDFs and 10 non-PDF files (`.png`, `.txt`).
2. Click "Start Batch Extraction".
3. **Expected Outcome**:
   - System filters out non-PDF files automatically.
   - Multi-core process pool executes extraction with live progress updates.
   - Generated CSV contains header matching defined keys (`_file_name,_file_path,_status,total_amount,vendor_address`) and 50 data rows.

---

## Automated Test Suite Execution

```bash
pytest tests/
```
