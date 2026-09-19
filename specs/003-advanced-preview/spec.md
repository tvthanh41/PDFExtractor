# Feature Specification: Advanced Preview

**Feature Branch**: `003-advanced-preview`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "now we need the preview extraction better. Currently, when we click on the preview button, it show up a message box. That is not good if we add many rule. And We want the output is a csv file, so instead of show a message box like that, we need to some how show it like excel. And of course, it still need some basic UI action like reduce/increase column size to view all of the content in case the value is a big string. Next, we need to be able to preview rule, so I believe you should add a button for each rule then we can preview each rule easier."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Spreadsheet-Like Preview & CSV Export (Priority: P1)

As a template creator, I want to view my extraction results in a spreadsheet-like interface with resizable columns and export them to a CSV file, so I can easily analyze large amounts of extracted data.

**Why this priority**: Message boxes cannot scale to display large quantities of rules or massive extracted text blocks. A spreadsheet UI is the industry standard for this type of data visualization.

**Independent Test**: Can be fully tested by clicking the "Preview Extraction" button and interacting with the spreadsheet popup, verifying column resizing, and clicking the export to CSV button to save a valid CSV file.

**Acceptance Scenarios**:

1. **Given** I have a PDF loaded and extraction rules defined, **When** I click "Preview Extraction", **Then** a popup opens containing a spreadsheet view with keys as columns and extracted values in rows.
2. **Given** the spreadsheet preview is open, **When** I drag a column header boundary, **Then** the column size changes.
3. **Given** the spreadsheet preview is open, **When** I click the CSV export button, **Then** I am prompted to save a CSV file containing the extracted data.

---

### User Story 2 - Per-Rule Detailed Preview (Priority: P2)

As a template creator, I want to click a preview button next to a specific rule to see its extracted value in a dedicated window, so I can easily verify complex or large extractions for that single rule without running a full extraction preview.

**Why this priority**: Testing individual rules accelerates template creation and debugging, allowing immediate visual feedback on complex text extractions.

**Independent Test**: Can be tested by clicking the "Preview" button next to a rule in the data table and ensuring the popup text box contains the expected extracted value.

**Acceptance Scenarios**:

1. **Given** the rules table contains one or more rules, **When** I view the table, **Then** I see a "Preview" action button for each rule.
2. **Given** I click the "Preview" button for a rule, **Then** a dedicated dialog box opens displaying the extracted text for just that rule, with support for scrolling large strings.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST replace the existing QMessageBox preview with a tabular spreadsheet interface.
- **FR-002**: System MUST allow users to resize columns in the tabular preview.
- **FR-003**: System MUST provide a function to export the tabular preview data to a valid CSV file on disk.
- **FR-004**: System MUST display an actionable "Preview" button for every rule within the main rules data table.
- **FR-005**: System MUST extract and display data for a single rule in a scrollable popup when the per-rule preview button is clicked.

### Key Entities

- **Preview Dialog**: A tabular user interface component capable of displaying dict-like extraction data.
- **Rule Preview Dialog**: A text-based user interface component capable of displaying large strings of extracted text for a single rule.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully resize columns in the preview interface.
- **SC-002**: A CSV file is successfully written to disk containing the correct extraction results.
- **SC-003**: A dedicated button is present and clickable for every row in the rules table.
- **SC-004**: Clicking a per-rule preview button displays a scrollable text area for reviewing large data strings.

## Assumptions

- Standard system CSV formatting (comma-separated, UTF-8 encoding) is acceptable for the export feature.
- The per-rule preview requires the PDF to be loaded on the canvas, identical to the full extraction preview.
