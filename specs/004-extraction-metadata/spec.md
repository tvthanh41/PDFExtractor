# Feature Specification: Extraction Metadata

**Feature Branch**: `004-extraction-metadata`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "the output csv and preview extraction should have some predefined key (which automatically added to all template, but it dont required user to setup). That include: - ffile name - file path - generated time - user: if you can find the user currently run that aplication then add this column, but if not we can skip. - template name: current template use."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automatic Metadata Inclusion (Priority: P1)

As a template creator or data processor, I want standard file and execution metadata (like file name, file path, template name, user, and timestamp) to be automatically appended to my extraction results, so that I can maintain an audit trail and trace the origins of extracted data without having to manually define these rules in every template.

**Why this priority**: When processing large batches of PDFs, distinguishing where data came from and when it was processed is critical for data governance and organization.

**Independent Test**: Can be tested by opening any PDF, running the "Preview Extraction" function (with or without custom rules), and verifying that the resulting spreadsheet and CSV contain the new metadata columns populated with correct system data.

**Acceptance Scenarios**:

1. **Given** a user triggers a preview extraction, **When** the results are generated, **Then** the output automatically includes the columns: "File Name", "File Path", "Generated Time", "User", and "Template Name".
2. **Given** the extraction is executed, **When** the "User" information cannot be reliably determined by the OS, **Then** the "User" column safely falls back to a default value (e.g., "Unknown") or is omitted gracefully.
3. **Given** a user is designing a template, **When** they view their rules list, **Then** they do not see these metadata rules cluttering their custom extraction rules list.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically inject predefined metadata key-value pairs into the final extraction dictionary before passing it to the preview dialog and CSV export.
- **FR-002**: System MUST inject the "File Name" of the processed PDF.
- **FR-003**: System MUST inject the absolute "File Path" of the processed PDF.
- **FR-004**: System MUST inject the "Generated Time" (current system timestamp) in a standard format (e.g., ISO 8601 or YYYY-MM-DD HH:MM:SS).
- **FR-005**: System MUST inject the "Template Name" currently being executed.
- **FR-006**: System MUST attempt to capture the current OS user ("User") and include it if available.
- **FR-007**: Metadata MUST NOT be stored as explicit rules inside the user's `.pdftpl` template files.

### Key Entities

- **Extraction Metadata**: System-generated contextual data appended to the rule-based extraction results.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of extracted CSVs and previews include the 5 specified metadata columns.
- **SC-002**: The template file (`.pdftpl`) schema remains unaffected and backwards compatible.
- **SC-003**: Metadata extraction takes negligible time (<10ms per document) and does not impact batch processing performance.

## Assumptions

- The standard Python `os` or `getpass` modules are sufficient for retrieving the current user.
- If the PDF has not been saved or exists purely in memory (which is currently impossible in this app as PDFs are opened from disk), the file path logic will handle it gracefully.
- The metadata keys will use standard capitalization (e.g., `File Name`, `Generated Time`) to distinguish them from user keys, or perhaps a prefix.
