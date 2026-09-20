# Feature Specification: Table Extraction

**Feature Branch**: `010-table-extraction`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "We also need to extract the table from pdf file but that isn't easy feature. Because table is very different thing so we can add table as a type of rule and also please add more advance config so that user can control how they can extract table because the table may behave differently in the pdf file."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Define Table Extraction Rule (Priority: P1)

Users need to be able to create a "Table" rule type within their template to instruct the system to look for tabular data instead of just plain text.

**Why this priority**: Without a specific rule type for tables, the system will treat tables as raw text blocks, which loses column/row structure.

**Independent Test**: Can be fully tested by creating a template, adding a Table rule, and verifying that the rule is saved correctly with table-specific metadata.

**Acceptance Scenarios**:

1. **Given** the user is editing a template, **When** they click "Add Rule", **Then** "Table" is available as a rule type alongside "Bounding Box" and "Anchor".
2. **Given** the user creates a Table rule, **When** they select a region on the canvas, **Then** the table region is recorded.

---

### User Story 2 - Advanced Table Configuration (Priority: P2)

Because tables vary wildly in how they are drawn (e.g., with or without border lines, varying column widths), users need advanced configuration options to guide the extraction engine.

**Why this priority**: Automated table extraction often fails without hints. Giving users configuration options ensures they can handle messy or borderless tables.

**Independent Test**: Can be fully tested by opening the configuration dialog for a Table rule and verifying the options are adjustable.

**Acceptance Scenarios**:

1. **Given** a Table rule has been created, **When** the user edits its properties, **Then** they see advanced options (e.g., "Has explicit borders", "Use custom column boundaries", "Header rows count").
2. **Given** the user sets advanced table options, **When** the rule is previewed, **Then** the extraction engine respects those hints.

---

### User Story 3 - Extract and Export Table Data (Priority: P1)

The system must extract the structured table data and export it meaningfully (e.g., as part of the CSV export, or as separate CSV files).

**Why this priority**: Extracting the table is useless if the structured rows and columns cannot be exported.

**Independent Test**: Run a batch extraction on a document with a table and verify the output format.

**Acceptance Scenarios**:

1. **Given** a template with a Table rule, **When** the user runs a batch extraction, **Then** the output accurately reflects the rows and columns of the table.

---

### Edge Cases

- What happens if a table spans multiple pages? (For this MVP, we will assume tables are constrained to the region defined on a single page, unless multi-page parsing is explicitly enabled).
- How does the system handle nested tables or merged cells? (Merged cells might be duplicated or left blank depending on the engine's capability).
- What if the user defines a table region but no table exists there? (Should return empty data or a warning).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to select "Table" as a new rule type when creating template rules.
- **FR-002**: System MUST provide an advanced configuration dialog for Table rules to adjust extraction strategies (e.g., borderless vs bordered, vertical strategy).
- **FR-003**: System MUST extract table data preserving the row and column structure.
- **FR-004**: System MUST export extracted table data appropriately during batch processing. Table data must be flattened and saved into the main CSV file as a JSON string.

### Key Entities 

- **Table Rule**: A specific type of extraction rule that targets tabular data and contains advanced parsing configurations.
- **Table Data**: A structured representation (rows and columns) of the extracted information.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully extract structured data from bordered and borderless tables.
- **SC-002**: Extracted table data maintains correct column alignment for at least 90% of standard invoices/reports.
- **SC-003**: Users can configure table extraction rules without needing to write code or regular expressions.

## Assumptions

- The underlying PDF extraction engine has native or reliable support for detecting tables within a bounding box.
- Tables are primarily horizontal (rows and columns) and text-based.
- Complex multi-page tables are out of scope for the initial MVP.
