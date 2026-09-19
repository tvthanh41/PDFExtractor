# Feature Specification: Advanced Rule Configuration

**Feature Branch**: `006-advanced-rule-config`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "In the template, we have some configuration which currently not for user to setup: `offset_distance` and `match_index`. We need to add the advance configuration the rule creation and rule edit GUI, so that user can set those value if they needed, we still keep default value as shown in the example. Please review if we need other setting that need to add to that advance configuration section."

## Background

Currently the **Rule Dialog** (`src/ui/rule_dialog.py`) exposes these fields for Anchor rules:
- Key Name
- Data Type
- Anchor Text
- Search Mode
- Direction

The following fields exist in the domain model but are **silently defaulted** with no way for users to change them:

### Anchor Rule hidden fields (`AnchorExtractionRule`)
| Field | Default | Meaning |
|-------|---------|---------|
| `offset_distance` | `150.0` | Maximum pixel distance from the anchor to search for a value. A higher value scans a wider area. |
| `match_index` | `0` | Which occurrence of the anchor text to use (0 = first, 1 = second, etc.) if the text appears multiple times on the page. |

### Bounding Box Rule hidden fields (`BoundingBoxExtractionRule`)
| Field | Default | Meaning |
|-------|---------|---------|
| `page_index` | `0` | Which page (0-based) to extract from. Currently hardcoded to `0`. |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Expose Anchor Rule Advanced Settings (Priority: P1)

When a user creates or edits an **Anchor** extraction rule, they can optionally expand an "Advanced Settings" section in the dialog and configure `offset_distance` and `match_index`. The section is collapsed by default and shows the current defaults so it doesn't clutter the basic workflow.

**Why this priority**: `offset_distance` and `match_index` are the most impactful hidden settings. An anchor with a short offset may miss values that are far away; a document with repeated labels (e.g., two "Total:" entries) can't be differentiated without `match_index`.

**Independent Test**: Create an anchor rule, expand Advanced Settings, change `offset_distance` to 300 and `match_index` to 1, save, and re-open the rule. The values must persist correctly.

**Acceptance Scenarios**:

1. **Given** the Rule Dialog is open for an Anchor rule, **When** the user clicks "Advanced Settings", **Then** a collapsible section expands showing `Offset Distance` and `Match Index` inputs with their current values.
2. **Given** Advanced Settings is expanded, **When** the user sets `offset_distance = 300.0` and `match_index = 1`, **Then** clicking Save creates a rule with those exact values.
3. **Given** a saved rule with non-default advanced values, **When** the user opens the edit dialog, **Then** the Advanced Settings section shows the saved values (not the defaults).
4. **Given** the user does not expand Advanced Settings, **When** the rule is saved, **Then** defaults (`offset_distance=150.0`, `match_index=0`) are used.

---

### User Story 2 - Expose Bounding Box `page_index` Setting (Priority: P2)

When a user creates or edits a **Bounding Box** rule, an "Advanced Settings" section exposes `page_index` so the user can extract from a page other than page 0 (e.g., the summary on the last page of a multi-page invoice).

**Why this priority**: `page_index` is important for multi-page documents, but secondary to the anchor settings which affect all anchor rules.

**Independent Test**: Create a bounding box rule, expand Advanced Settings, set `page_index = 2`, save, and re-open. The value must persist.

**Acceptance Scenarios**:

1. **Given** the Rule Dialog is open for a Bounding Box rule, **When** the user clicks "Advanced Settings", **Then** a `Page Index` input appears with the current value (default: `0`).
2. **Given** the user sets `page_index = 2`, **When** the rule is saved, **Then** the serialized rule has `"page_index": 2`.
3. **Given** a saved rule with `page_index = 3`, **When** the user opens the edit dialog, **Then** the Page Index field shows `3`.

---

### Edge Cases

- What happens if `offset_distance` is set to `0`? → The system should still attempt to find immediately adjacent values (the field has `ge=0` constraint in the model — allow `0`).
- What happens if `match_index` is larger than the number of occurrences? → The extraction strategy already returns `None` gracefully in this case.
- What happens if `page_index` exceeds the document's page count? → The extraction strategy already returns `None` gracefully.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Rule Dialog MUST add a collapsible "Advanced Settings" section for **Anchor** rules containing:
  - `Offset Distance` (float spinner, min 0, default 150.0)
  - `Match Index` (integer spinner, min 0, default 0)
- **FR-002**: The Rule Dialog MUST add a collapsible "Advanced Settings" section for **Bounding Box** rules containing:
  - `Page Index` (integer spinner, min 0, default 0)
- **FR-003**: Advanced Settings MUST be collapsed by default, and expand on user interaction.
- **FR-004**: When editing an existing rule with non-default advanced values, those values MUST be pre-populated in the advanced section.
- **FR-005**: Saved rules MUST correctly serialize all advanced values to the `.pdftpl` JSON.

### Key Entities

- **`AnchorExtractionRule`**: Adds UI controls for `offset_distance` (float) and `match_index` (int).
- **`BoundingBoxExtractionRule`**: Adds UI control for `page_index` (int); current hardcoded `page_index=0` in `_create_rule()` to be replaced by the spinner value.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All advanced fields round-trip correctly (set → save → re-open → same values displayed).
- **SC-002**: Default values are used when Advanced Settings are not touched.
- **SC-003**: The basic (non-advanced) rule creation workflow is unchanged — users who never open Advanced Settings should notice no difference.

## Assumptions

- "Collapsible" is implemented via a toggle button that shows/hides the advanced fields group, as PySide6 does not have a native collapse widget.
- No new domain model fields are required; all fields already exist in the models.
- The `BoundingBoxExtractionRule.page_index` field is 0-based (consistent with `page.get_text("words")` indexing in PyMuPDF).
