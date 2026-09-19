# Feature Specification: Fix Box Rule UI and Coordinate Mapping

**Feature Branch**: `[008-fix-box-rule-ui]`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "the box rule not work correctly, there is different between the coordinate in PyMuPDF and PyQT6 so when I choose a region in file, it seems like pick another region and the extract value isn't correct. One more thing, it seems like we cannot choose the region again if we already added box rule. When click to the rule, it show only the dialog to change the parameter but not allow to choose a new region. The list of rule now also doesn't allow delete. One added we have no way to delete. So the UI seem not very friendly. Please review the UI design, we cannot keep showing UI like this, very disappointed user experience."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Accurate Region Selection (Priority: P1)

As a user, I want the region I select on the PDF canvas to accurately map to the extracted text, so that I can reliably extract the intended data.

**Why this priority**: Core functionality is broken if the coordinates don't map correctly between the display and the extraction engine.

**Independent Test**: Can be fully tested by selecting a known text box and verifying the extracted output perfectly matches the selection.

**Acceptance Scenarios**:

1. **Given** a loaded PDF, **When** I draw a bounding box around a specific text region, **Then** the extracted text matches exactly what was inside the visual bounding box.

---

### User Story 2 - Reselect Region for Existing Rule (Priority: P2)

As a user, I want to be able to redefine the bounding box region for an existing box rule, so that I don't have to delete and recreate the rule if I made a mistake.

**Why this priority**: Improves usability and error recovery for rule creation.

**Independent Test**: Can be fully tested by creating a rule, editing it, and successfully drawing a new region on the canvas.

**Acceptance Scenarios**:

1. **Given** an existing box rule, **When** I edit the rule, **Then** I have an option to reselect the region on the PDF canvas.
2. **Given** I am reselecting a region, **When** I draw a new box, **Then** the rule's coordinates are updated to the new selection.

---

### User Story 3 - Delete Existing Rules (Priority: P3)

As a user, I want to be able to delete rules from the rule list, so that I can remove mistakes or obsolete rules from my template.

**Why this priority**: Essential basic CRUD operation for managing template rules.

**Independent Test**: Can be fully tested by adding a rule and then deleting it from the list.

**Acceptance Scenarios**:

1. **Given** a list of existing rules, **When** I select a rule and choose to delete it, **Then** the rule is removed from the template and the list updates.

---

### Edge Cases

- What happens when a user starts reselecting a region but cancels? The original region should be preserved.
- How does the system handle coordinate scaling when the user zooms in or out on the PDF canvas?
- What happens if the selected region goes out of the page bounds?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accurately translate coordinate systems between the UI rendering (PyQt6) and the PDF extraction engine (PyMuPDF).
- **FR-002**: System MUST provide a mechanism (e.g., a "Reselect Region" button) within the rule edit dialog or directly on the canvas to allow users to update the bounding box for an existing rule.
- **FR-003**: System MUST provide a "Delete" action in the rule list UI for users to remove selected rules.
- **FR-004**: System MUST prompt for confirmation before deleting a rule.

### Key Entities *(include if feature involves data)*

- **Bounding Box Rule**: Requires updated coordinates when reselected.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% accurate text extraction matching the visually selected bounding box across different PDF sizes and DPIs.
- **SC-002**: Users can update an existing rule's region in fewer than 3 clicks.
- **SC-003**: Users can delete a rule in 2 clicks (including confirmation).

## Assumptions

- Users use a standard mouse or trackpad for region selection.
- The coordinate translation issue is solely a scaling/origin offset issue between the rendering library and the PDF parser.
- Rule deletion does not have cascading effects on other rules.
