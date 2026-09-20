# Research & Decisions: Table Extraction

## 1. PDF Table Extraction Engine

- **Decision**: Use PyMuPDF (`fitz.Page.find_tables()`).
- **Rationale**: PyMuPDF 1.23+ provides native table detection via `page.find_tables(clip=rect, strategy=...)` which accepts a bounding box rect (`clip`) and extraction strategy parameters. Since PyMuPDF is already the core dependency of this application (`PyMuPDF>=1.23.0`), utilizing native `find_tables` avoids adding heavy external dependencies such as Java (`tabula-py`) or OpenCV (`camelot-py`).
- **Alternatives Considered**:
  - `pdfplumber`: Excellent table extraction, but adds another PDF parsing dependency alongside PyMuPDF, potentially causing discrepancy in page dimensions and coordinates.
  - `camelot-py` / `tabula-py`: Require Ghostscript or Java runtime environment, violating desktop single-binary packaging goal (PyInstaller).

## 2. Rule Model & Pydantic Union Serialization

- **Decision**: Define `TableExtractionRule` inheriting from `ExtractionRuleBase` with `rule_type: RuleType = RuleType.TABLE`. Include `page_index: int`, `box: BoundingBox`, and `table_config: TableConfig`.
- **Rationale**: Keeps domain models clean and compliant with Constitution Principle III. Pydantic v2 automatically handles discriminated unions based on `rule_type`.
- **Alternatives Considered**:
  - Adding table parameters into `BoundingBoxExtractionRule`: Messy, causes optional null fields for standard bounding box rules.
  - Raw dict configuration: Violates Pydantic model contract.

## 3. Data Representation & CSV Export Flattening

- **Decision**: `TableExtractionStrategy.extract()` extracts the table as a 2D list of strings `List[List[str]]`. During CSV export, `CSVExporter` checks if an extracted value is a list/dict and serializes it using `json.dumps(val, ensure_ascii=False)`.
- **Rationale**: Directly satisfies requirement FR-004 ("Table data must be flattened and saved into the main CSV file as a JSON string").
- **Alternatives Considered**:
  - Exporting a separate CSV per extracted table: Breaks batch single-file pipeline expectation unless requested.
  - Unrolling table columns into dynamically generated main CSV headers: Can lead to mismatched columns across different documents in batch processing if row/column counts vary.

## 4. PySide6 UI Configuration Integration

- **Decision**: Update `RuleDialog` to dynamically show/hide table configuration controls when `RuleType.TABLE` is selected. Render table bounding boxes on canvas with distinct styling (e.g., emerald green border with table grid icon).
- **Rationale**: Provides clear visual feedback for rule authoring while maintaining consistent UX across rule types.
