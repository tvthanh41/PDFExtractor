# Feature Specification: Batch Job Configuration & Template Naming Fixes

**Feature Branch**: `005-batch-config`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "when I load a template file named test, the new open tab still named as New Template and then when we run batch job, the result file will populate the template name as 'New Template' which is incorrect. One more thing, when we select run batch job, it should show a dialog allow we select and view current template and current folder to run instead of current behavior, in case user choose the wrong folder or wrong template, they cannot do anything until the batch job finish, which is very disappointed."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Template Naming Persistence (Priority: P1)

When a user loads an existing template, the tab title and the template metadata must accurately reflect the loaded template's name (e.g., derived from the filename or internal metadata) instead of defaulting to "New Template".

**Why this priority**: Essential for data integrity. Extraction output metadata must accurately reflect the template used.

**Independent Test**: Can be fully tested by loading an existing template named "test.pdftpl", verifying the UI tab says "test", and verifying that batch extractions label the template as "test" in the output.

**Acceptance Scenarios**:

1. **Given** an existing template file `test.pdftpl`, **When** the user loads it via "Open Template", **Then** the workspace tab is named "test".
2. **Given** the loaded template `test.pdftpl`, **When** the user runs an extraction, **Then** the "template name" column in the output is populated with "test" (not "New Template").

---

### User Story 2 - Batch Job Configuration Dialog (Priority: P1)

When a user initiates a Batch Job, they are presented with a configuration dialog that clearly displays the selected template and input folder. The user must explicitly confirm the job to start it, giving them a chance to review or cancel if they made a mistake.

**Why this priority**: Prevents user frustration and accidental executions on large directories which lock the application state.

**Independent Test**: Can be tested by clicking "Run Batch Job", selecting the paths, and ensuring a confirmation dialog appears containing the chosen paths before any processing begins.

**Acceptance Scenarios**:

1. **Given** the user selects a template and folder for a batch job, **When** the selections are complete, **Then** a Batch Configuration Dialog appears showing the chosen Template Path and Input Folder Path.
2. **Given** the Batch Configuration Dialog is open, **When** the user clicks "Cancel", **Then** the batch job is aborted and no extraction occurs.
3. **Given** the Batch Configuration Dialog is open, **When** the user clicks "Start Batch", **Then** the batch extraction begins.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST correctly assign the template name from the filename or JSON metadata when loading an existing `.pdftpl` file.
- **FR-002**: System MUST update the UI Workspace Tab title to match the loaded template name.
- **FR-003**: System MUST prompt the user with a Batch Configuration Dialog after selecting the template and input folder, but before starting the batch extraction.
- **FR-004**: The Batch Configuration Dialog MUST display the selected Template Path, Input Folder Path, and Output CSV Path.
- **FR-005**: The Batch Configuration Dialog MUST contain "Start" and "Cancel" actions.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of loaded templates display their correct name in the UI and extraction outputs.
- **SC-002**: Users can abort a misconfigured batch job 100% of the time before execution begins.

## Assumptions

- The template name can be safely derived from the file's basename (without the `.pdftpl` extension) if the JSON does not contain a specific `name` property.
- The Batch Configuration dialog will block the main window until accepted or rejected (modal).
