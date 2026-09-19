# Tasks: Batch Job Configuration & Template Naming Fixes

## Phase 1: Setup
- [X] T001 Create `src/ui/batch_config_dialog.py` placeholder

## Phase 2: Foundational
(None needed, existing project)

## Phase 3: User Story 1 - Template Naming Persistence (Priority: P1)
**Goal**: Ensure loaded templates reflect their correct name in the UI and outputs.
**Independent Test**: Load an existing template and see the correct tab name.

- [X] T002 [P] [US1] Update `load` method in `src/services/template_repository.py` to use filename basename as the template name.
- [X] T003 [P] [US1] Update `save_template` in `src/controllers/template_controller.py` to sync `self.template.name` with the saved filename.
- [X] T004 [US1] Ensure `AppController.open_template` in `src/controllers/app_controller.py` correctly uses `template.name` for the tab title (already does, but verify it works with the repo change).

## Phase 4: User Story 2 - Batch Job Configuration Dialog (Priority: P1)
**Goal**: Show a confirmation dialog before starting batch extraction.
**Independent Test**: Run batch extraction, select files, and verify the dialog appears with "Start Batch" and "Cancel" buttons.

- [X] T005 [P] [US2] Implement `BatchConfigDialog` UI in `src/ui/batch_config_dialog.py`.
- [X] T006 [US2] Modify `run_batch` in `src/controllers/app_controller.py` to launch `BatchConfigDialog` and await acceptance before execution.
- [X] T007 [P] [US2] Add integration test for batch config dialog interaction in `tests/integration/test_batch_config.py`.

## Phase 5: Polish & Cross-Cutting Concerns
- [X] T008 Run quickstart validation scenarios — all 14 tests pass.

## Dependencies & Execution Order
- Phase 3 (US1) and Phase 4 (US2) can be done in parallel.
- Within US1, T002 and T003 can be parallelized.
- Within US2, T005 must be done before T006.
