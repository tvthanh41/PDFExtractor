# Tasks: App Installer & Branding

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for bundling

- [x] T001 Add `pyinstaller` to `requirements.txt` (or install it in the local environment)
- [x] T002 [P] Create `resources/` directory in the repository root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Assets that MUST be complete before building

- [x] T003 Save the generated app icon as `resources/app_icon.png`
- [x] T004 Convert `resources/app_icon.png` to `resources/app_icon.ico`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Standalone Application Bundle (Priority: P1) 🏆 MVP

**Goal**: Package the PySide6 application as a standalone executable.

**Independent Test**: Build the app and verify it launches.

### Implementation for User Story 1

- [x] T005 [P] [US1] Create `build_app.py` in the repository root to invoke PyInstaller programmatically (using `--noconsole` and `--onefile`).
- [x] T006 [US1] Update `build_app.py` to correctly bundle the `src/i18n/locales/` directory into the executable using `--add-data`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Professional App Icon (Priority: P2)

**Goal**: Configure the custom app icon for both the UI window and the Windows executable.

**Independent Test**: Verify the taskbar icon and the file explorer icon.

### Implementation for User Story 2

- [x] T007 [P] [US2] Update `build_app.py` to include the `--icon=resources/app_icon.ico` argument for PyInstaller.
- [x] T008 [P] [US2] Update `src/main.py` (or `main_window.py`) to load `resources/app_icon.png` and set it via `app.setWindowIcon()`.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Author and Version Information (Priority: P3)

**Goal**: Embed metadata into the executable and provide an About dialog in the UI.

**Independent Test**: Check executable properties and the UI About dialog.

### Implementation for User Story 3

- [x] T009 [P] [US3] Create `file_version_info.txt` in the repository root with standard PyInstaller version metadata (Version 1.0.0, Author: github-spec-kit).
- [x] T010 [US3] Update `build_app.py` to include the `--version-file=file_version_info.txt` argument.
- [x] T011 [P] [US3] Add a "Help" -> "About" menu action in `src/ui/main_window.py`.
- [x] T012 [US3] Implement the About dialog display logic (using `QMessageBox.about`) showing version and author details.

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T013 [P] Run quickstart.md validation to ensure the build succeeds and all features work.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel
- **Polish (Final Phase)**: Depends on all desired user stories being complete
