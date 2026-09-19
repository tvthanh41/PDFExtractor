# Implementation Tasks: Modify Rule via Popup GUI

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify PySide6 and pytest test runner environment

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Modify Existing Rule (Priority: P1) 🏆 MVP

**Goal**: Users can edit an existing rule using a dedicated popup dialog so that they have a clear, spacious interface to configure complex rule properties without struggling with inline table cells.

**Independent Test**: Can be tested by creating a rule, closing the dialog, and reopening it for editing to verify that changes are saved and reflected.

### Tests for User Story 1 (OPTIONAL)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T002 [P] [US1] Integration test for modifying a rule via dialog in `tests/ui/test_rule_dialog.py`
- [x] T003 [P] [US1] Unit test verifying inline editing is disabled in `tests/ui/test_rule_dialog.py`

### Implementation for User Story 1

- [x] T004 [P] [US1] Disable inline editing on the rules data table (`setEditTriggers`) in `src/ui/workspace_tab.py`
- [x] T005 [US1] Update `RuleDialog.__init__` signature to accept `rule: ExtractionRule = None` in `src/ui/rule_dialog.py`
- [x] T006 [US1] Pre-populate `RuleDialog` inputs if `rule` is provided in `src/ui/rule_dialog.py`
- [x] T007 [US1] Return modified rule from `RuleDialog` preserving `rule_id` in `src/ui/rule_dialog.py`
- [x] T008 [US1] Connect table double-click to `edit_rule` slot in `src/controllers/template_controller.py`
- [x] T009 [US1] Implement `edit_rule` in `TemplateController` to handle rule updating in template model in `src/controllers/template_controller.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Preview and Canvas Highlight (Priority: P2)

**Goal**: System shows a preview and highlights the bounding box on the PDF canvas when a rule is selected.

**Independent Test**: Can be tested by selecting different rules in the list and verifying the canvas highlighting updates accordingly.

### Implementation for User Story 2

- [x] T010 [P] [US2] Add `selected_rule_id` state to `TemplateController` in `src/controllers/template_controller.py`
- [x] T011 [US2] Handle table single-click to update `selected_rule_id` and trigger canvas repaint in `src/controllers/template_controller.py`
- [x] T012 [US2] Update canvas rendering to highlight the bounding box for `selected_rule_id` in `src/ui/pdf_canvas.py`
- [x] T013 [US2] Display preview of extracted data for the selected rule in `src/ui/workspace_tab.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T014 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 UI changes but is functionally independent.

### Parallel Opportunities

- Tests (T002, T003) and UI updates (T004) can be developed in parallel.
- Controller logic (T008, T009) depends on Dialog changes (T005-T007).

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2
2. Complete Phase 3: User Story 1
3. **STOP and VALIDATE**: Test User Story 1 independently

### Incremental Delivery

1. Complete Setup + Foundational
2. Add User Story 1 -> Test independently -> Deliver MVP
3. Add User Story 2 -> Test independently -> Deliver
