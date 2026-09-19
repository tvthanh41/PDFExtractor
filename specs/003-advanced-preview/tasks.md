# Tasks: Advanced Preview

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Verify project structure per implementation plan

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

*(No foundational prerequisites required for this UI extension feature)*

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Spreadsheet-Like Preview & CSV Export (Priority: P1) 🚀 MVP

**Goal**: View extraction results in a spreadsheet-like interface with resizable columns and export them to a CSV file.

**Independent Test**: Can be fully tested by clicking the "Preview Extraction" button and interacting with the spreadsheet popup, verifying column resizing, and clicking the export to CSV button to save a valid CSV file.

### Implementation for User Story 1

- [X] T002 [US1] Create `PreviewDialog` in `src/ui/preview_dialog.py` containing a `QTableWidget` and CSV export logic
- [X] T003 [US1] Modify `src/controllers/template_controller.py` to update `preview_extraction` to instantiate and execute `PreviewDialog`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Per-Rule Detailed Preview (Priority: P2)

**Goal**: Click a preview button next to a specific rule to see its extracted value in a dedicated window.

**Independent Test**: Can be tested by clicking the "Preview" button next to a rule in the data table and ensuring the popup text box contains the expected extracted value.

### Implementation for User Story 2

- [X] T004 [US2] Create `RulePreviewDialog` in `src/ui/rule_preview_dialog.py` with a `QTextEdit` for single-rule text preview
- [X] T005 [US2] Modify `src/ui/workspace_tab.py` to add "Actions" column and "Preview" buttons using `setCellWidget`
- [X] T006 [US2] Modify `src/controllers/template_controller.py` to implement `preview_single_rule` logic connected to the new buttons

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T007 Run quickstart.md validation by restarting the app and testing end-to-end flows

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 ➔ P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on US1, can be built independently

### Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational ➔ Foundation ready
2. Add User Story 1 ➔ Test independently ➔ Deploy/Demo (MVP!)
3. Add User Story 2 ➔ Test independently ➔ Deploy/Demo
4. Each story adds value without breaking previous stories
