# Tasks: Extraction Metadata

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Verify project structure per implementation plan

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

*(No foundational prerequisites required for this feature)*

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Automatic Metadata Inclusion (Priority: P1) 🚀 MVP

**Goal**: Standard file and execution metadata (like file name, file path, template name, user, and timestamp) should be automatically appended to extraction results.

**Independent Test**: Can be tested by opening any PDF, running the "Preview Extraction" function (with or without custom rules), and verifying that the resulting spreadsheet and CSV contain the new metadata columns populated with correct system data.

### Implementation for User Story 1

- [X] T002 [P] [US1] Modify `src/controllers/template_controller.py` to inject `file name`, `file path`, `generated time`, `user`, and `template name` into `results` dictionary in `preview_extraction`.
- [X] T003 [P] [US1] Modify `src/services/csv_exporter.py` to add `file name`, `file path`, `generated time`, `user`, and `template name` to `CSVExporter.export` headers, and inject the values during row mapping.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T004 Restart the application and test preview and CSV export flows (Quickstart validation).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3+)**: Depends on Foundational completion
- **Polish (Final Phase)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).

### Parallel Opportunities

- T002 and T003 can be executed entirely in parallel because they touch completely different files (`template_controller.py` and `csv_exporter.py`) and do not have mutual code dependencies.
