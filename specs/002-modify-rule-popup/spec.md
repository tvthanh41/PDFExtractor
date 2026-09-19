# Feature Specification: Modify Rule via Popup GUI

**Feature Branch**: `002-modify-rule-popup`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "Allow users to modify rules via a popup GUI instead of inline editing. When a rule is selected, show a preview, and highlight the bounding box on the canvas if it is a box rule."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Modify Existing Rule (Priority: P1)

As a template creator, I want to edit an existing rule using a dedicated popup dialog so that I have a clear, spacious interface to configure complex rule properties without struggling with inline table cells.

**Why this priority**: Modifying rules is a core user action. Moving from inline editing to a popup makes the application robust and user-friendly, paving the way for more complex rule configurations.

**Independent Test**: Can be tested by creating a rule, closing the dialog, and reopening it for editing to verify that changes are saved and reflected.

**Acceptance Scenarios**:

1. **Given** a rule exists in the template, **When** I trigger an edit action on the rule, **Then** a popup dialog opens populated with the rule's current properties.
2. **Given** the popup dialog is open, **When** I change properties and save, **Then** the rule is updated in the list without creating a duplicate.
3. **Given** the rule list, **When** I try to type directly into the table cells, **Then** the cells are read-only to prevent inline editing.

---

### User Story 2 - Preview and Canvas Highlight (Priority: P2)

As a template creator, I want the system to show a preview and highlight the bounding box on the PDF canvas when I select a rule, so I can visually verify what data the rule is targeting.

**Why this priority**: Immediate visual feedback is crucial for validating extraction logic before running batch processes.

**Independent Test**: Can be tested by selecting different rules in the list and verifying the canvas highlighting updates accordingly.

**Acceptance Scenarios**:

1. **Given** I have a bounding box rule, **When** I select it in the list, **Then** the corresponding bounding box is visually highlighted on the document canvas.
2. **Given** I have any rule selected, **When** I select it, **Then** a preview of the extracted data for that specific rule is displayed.
3. **Given** I deselect a rule, **When** the selection clears, **Then** the canvas highlight is removed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a mechanism to edit an existing rule via a popup dialog.
- **FR-002**: System MUST disable inline editing on the rules data table.
- **FR-003**: System MUST highlight the associated bounding box on the PDF canvas when a bounding box rule is selected.
- **FR-004**: System MUST clear the canvas highlight when no bounding box rule is selected.
- **FR-005**: System MUST present a preview of the extracted data for the currently selected rule.

### Key Entities

- **Extraction Rule**: Contains configuration (key name, anchor, search mode, bounding box coordinates).
- **Canvas Visualizer**: The component responsible for rendering PDF pages and overlaying visual elements like bounding boxes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can edit all properties of a rule via the popup dialog.
- **SC-002**: Visual highlighting of the bounding box appears on the canvas when a box rule is selected.
- **SC-003**: The table inline editing is entirely disabled, directing all edits through the popup workflow.
- **SC-004**: The data preview updates correctly based on the selected rule.

## Assumptions

- We will reuse the existing `RuleDialog` for editing by passing the selected rule into it for pre-population.
- The PDF canvas already supports drawing bounding boxes; we simply need to trigger a "highlight" or "select" state for the correct box.
