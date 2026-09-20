# Quickstart & Validation Guide: Multi-Page Navigation and Pattern-Based Table Detection

## Prerequisites

1. Active Python environment with required dependencies:
   ```powershell
   .venv\Scripts\pip install -r requirements.txt
   .venv\Scripts\pip install pymupdf4llm
   ```

2. Run automated tests to verify the baseline:
   ```powershell
   .venv\Scripts\pytest
   ```

---

## Validation Scenarios

### Scenario 1: Multi-Page Viewing & Page Indexing

1. Start the desktop application:
   ```powershell
   .venv\Scripts\python src/main.py
   ```
2. Open a multi-page PDF document (e.g. 3 or more pages).
3. Verify the pagination controls at the bottom of the canvas:
   - "◀" (Previous) is initially disabled on page 1.
   - Page spinbox shows `1`, total label shows `/ 3`.
   - "▶" (Next) is enabled.
4. Click "▶" to navigate to Page 2. Verify canvas immediately re-renders page 2.
5. Click "Add Rule" while on Page 2:
   - The Rule Dialog opens with `Page Index` defaulted to `2` (display) / `1` (0-indexed).
   - Save an anchor rule. Verify the rule table displays `Page: 2`.

---

### Scenario 2: Dynamic Pattern Table Boundary Detection

1. On a document containing a line-item table with variable rows:
2. Open "Add Rule" -> Select Rule Type: `TABLE`.
3. Choose Boundary Mode: `Pattern Match`:
   - Set Start Pattern: `Item Description` (Include Start: checked).
   - Set End Pattern: `Subtotal` (Include End: unchecked).
   - Occurrence Skip: `0`.
4. Click "Test Extraction" in Rule Dialog:
   - Verify that the table bounding box is dynamically computed between "Item Description" and "Subtotal".
   - Verify extracted rows correspond exactly to the table rows between those markers.

---

### Scenario 3: Occurrence Filtering (`skip_k`) on Repeated Anchors

1. On a document with multiple "Date:" occurrences:
2. Create an Anchor Search rule:
   - Anchor Text: `Date:`
   - Match Occurrence / Skip: `1` (skip first match, select 2nd match).
3. Test extraction:
   - Verify the value extracted is from the 2nd "Date:" on that page, ignoring the 1st.

---

### Scenario 4: PyMuPDF4LLM Engine Extraction

1. Open a table rule with borderless columns.
2. In Advanced Settings, select Engine: `PyMuPDF4LLM`.
3. Click "Test Extraction":
   - Verify that markdown table heuristic parsing cleanly separates columns without merging cells.
