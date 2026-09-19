# Implementation Tasks: Fix Box Rule UI and Coordinate Mapping

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure
*(No specific setup tasks required as this is an existing project)*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented
*(No foundational structural changes required)*

---

## Phase 3: User Story 1 - Accurate Region Selection (Priority: P1) ⭐ MVP

**Goal**: Ensure coordinate mapping between UI and PyMuPDF correctly accounts for CropBox offsets.

**Independent Test**: Can be fully tested by selecting a known text box and verifying the extracted output perfectly matches the selection.

### Implementation for User Story 1

- [x] T001 [P] [US1] Update `PdfService.get_page_dimensions` to return the full `page.rect` (x0, y0, width, height) in `src/services/pdf_service.py`
- [x] T002 [US1] Update `BoundingBoxExtractionStrategy.extract` to use `page.rect.x0` and `y0` when calculating points in `src/strategies/bounding_box_strategy.py`
- [x] T003 [US1] Update `AnchorExtractionStrategy.extract` to use `page.rect.x0` and `y0` when calculating points in `src/strategies/anchor_strategy.py`

**Checkpoint**: At this point, coordinate mapping should perfectly match visual selection.

---

## Phase 4: User Story 2 - Reselect Region for Existing Rule (Priority: P2)

**Goal**: Allow users to redefine the bounding box region for an existing rule.

**Independent Test**: Can be fully tested by creating a rule, clicking to reselect its region, and drawing a new box on the canvas.

### Implementation for User Story 2

- [x] T004 [P] [US2] Add a "Reselect Region" button to the rule controls in `src/ui/workspace_tab.py`
- [x] T005 [US2] Implement `reselect_rule_region(self, index: int)` handler in `src/controllers/template_controller.py`
- [x] T006 [US2] Wire the "Reselect Region" button to trigger the new canvas selection mode via the controller

**Checkpoint**: Users can now modify regions without deleting and recreating rules.

---

## Phase 5: User Story 3 - Delete Existing Rules (Priority: P3)

**Goal**: Allow users to delete rules from the template.

**Independent Test**: Can be fully tested by adding a rule and deleting it from the list.

### Implementation for User Story 3

- [x] T007 [P] [US3] Add a "Delete Rule" button and confirmation dialog in `src/ui/workspace_tab.py`
- [x] T008 [US3] Implement `delete_rule(self, index: int)` to remove rules from `self.template.rules` in `src/controllers/template_controller.py`
- [x] T009 [US3] Update the UI table and clear previews when a rule is deleted in `src/controllers/template_controller.py`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T010 [P] Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: N/A
- **Foundational (Phase 2)**: N/A
- **User Stories (Phase 3+)**: US1, US2, and US3 are largely independent and can be implemented in parallel.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent. Core logic fix.
- **User Story 2 (P2)**: Independent UI fix.
- **User Story 3 (P3)**: Independent UI fix.

### Parallel Opportunities

- T001, T004, and T007 can be executed in parallel as they touch different parts of the system or add unconnected UI elements.

---

## Parallel Example: User Story 1

```bash
# Launch independent tasks:
Task: "Update PdfService.get_page_dimensions to return the full page.rect (x0, y0, width, height) in src/services/pdf_service.py"
Task: "Add a 'Reselect Region' button to the rule controls in src/ui/workspace_tab.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1 (Coordinate Fix).
2. **STOP and VALIDATE**: Ensure extraction matches selection perfectly.

### Incremental Delivery

1. Deliver User Story 1 (Core fix).
2. Add User Story 2 (Reselect Region).
3. Add User Story 3 (Delete Rule).
