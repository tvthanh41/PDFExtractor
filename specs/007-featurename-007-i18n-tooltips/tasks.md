# Tasks: UI Localisation & Tooltips (i18n)

**Feature**: 007-i18n-tooltips
**Branch**: `007-featurename-007-i18n-tooltips`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the i18n package skeleton and English locale file that all other tasks depend on.

- [ ] T001 Create `src/i18n/__init__.py` (empty package init)
- [ ] T002 [P] Create `src/i18n/locales/` directory with full `en.json` English string catalogue per data-model.md key table
- [ ] T003 [P] Write unit tests (failing) for `Translator`, `LocaleLoader`, and `PreferencesService` in `tests/unit/test_i18n.py`

**Checkpoint**: `en.json` exists with all keys; failing tests define the contract.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core i18n services that ALL UI migrations and the Settings dialog depend on.

> **⚠ CRITICAL**: No UI task can begin until T004–T007 are complete.

- [X] T004 Implement `Translator` class with `load(active, fallback)` and `translate(key)` fallback chain in `src/i18n/translator.py`; expose module-level `translator` instance and `t(key)` function
- [X] T005 [P] Implement `LocaleLoader` class with `discover()` and `load(code)` class methods in `src/i18n/locale_loader.py`
- [X] T006 [P] Implement `PreferencesService` with `get/set/get_language/set_language` backed by `~/.pdftpl_prefs.json` in `src/services/preferences_service.py`
- [X] T007 Update `src/main.py` to bootstrap i18n at startup: load language preference, load active locale + English fallback, initialise `translator` before any window is created


**Checkpoint**: `uv run pytest tests/unit/test_i18n.py -v` — all i18n unit tests pass.

---

## Phase 3: User Story 1 — String Catalogue & Tooltip Infrastructure (Priority: P1) 🎯 MVP

**Goal**: Every hard-coded UI string is replaced with `t(key)` calls. Every interactive element gets a `setToolTip(t("tooltip.xxx"))` call. App launches and displays correctly in English.

**Independent Test**: Launch app — all labels, buttons, table headers, and dialog titles display correct English text; hovering over any element shows a tooltip.

### Implementation

- [X] T008 [US1] Migrate `src/ui/main_window.py`: replace all string literals with `t()` calls; add Edit menu with Settings... action; add `setToolTip()` on menu actions
- [X] T009 [US1] Migrate `src/ui/workspace_tab.py`: replace all string literals with `t()` calls; add `setToolTip()` on all buttons and table column headers
- [X] T010 [US1] Migrate `src/ui/rule_dialog.py`: replace all string literals with `t()` calls; add `setToolTip()` on all inputs, combos, spinners, and toggle buttons
- [X] T011 [US1] Migrate `src/ui/batch_config_dialog.py`: replace all string literals with `t()` calls; add `setToolTip()` on all path fields and buttons
- [X] T012 [P] [US1] Migrate `src/ui/preview_dialog.py` and `src/ui/rule_preview_dialog.py`: replace all string literals with `t()` calls

**Checkpoint**: App launches, all strings display correctly in English, tooltips visible on hover.

---

## Phase 4: User Story 2 — Tooltips on All UI Elements (Priority: P1)

**Goal**: Verify every interactive element has a tooltip. Fill any gaps missed in US1 migration.

**Independent Test**: Manually hover over every button, field, and combo in all dialogs — no element is tooltip-free.

### Implementation

- [X] T013 [US2] Audit all dialogs and widgets for missing tooltips; add any missing `setToolTip(t("tooltip.xxx"))` calls across all UI files; add corresponding keys to `en.json` if any are missing
- [X] T014 [P] [US2] Add tooltip keys to `en.json` for any elements discovered in the audit (T013)

**Checkpoint**: Quickstart Scenario 1 (all tooltips visible) passes manually.

---

## Phase 5: User Story 3 — Language Setting & Runtime Switching (Priority: P2)

**Goal**: Settings dialog allows language selection; preference is persisted and loaded on next launch. Language list is dynamically discovered from `locales/`.

**Independent Test**: Select a language in Settings, restart — that language is loaded. Add a new `*.json` locale file without code changes — it appears in the Settings dropdown.

### Implementation

- [X] T015 [US3] Create `src/ui/settings_dialog.py`: `QDialog` with language `QComboBox` populated from `LocaleLoader.discover()`, OK/Cancel buttons; on accept calls `PreferencesService.set_language(code)` and shows restart info message
- [X] T016 [US3] Wire Settings dialog into `AppController` and `MainWindow`: add `open_settings()` method to `AppController`; connect Edit → Settings... menu action
- [ ] T017 [P] [US3] Create Vietnamese placeholder locale `src/i18n/locales/vi.json` with `_meta.language_name` and a minimal set of translated keys to validate multi-language discovery works

**Checkpoint**: Quickstart Scenarios 2, 3, 4 pass — language list dynamic, preference persists across restart.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T018 Run full test suite: `uv run pytest tests/ -v`
- [X] T019 Verify no remaining hard-coded display strings in `src/ui/` using `grep -r "QPushButton\|QLabel\|addMenu\|addAction" src/ui/ | grep -v "t(\""` as a sanity check
- [X] T020 Run quickstart.md manual validation scenarios 1–4

---

## Dependencies & Execution Order

```
T001, T002, T003 (parallel setup)
    ↓
T004 → T005, T006 (T005 and T006 parallel after T004)
    ↓
T007 (depends on T004, T005, T006)
    ↓
T008, T009, T010, T011, T012 (all US1 — same package, do sequentially)
    ↓
T013, T014 (US2 audit — after all UI files migrated)
    ↓
T015, T016, T017 (US3 — T015 before T016; T017 parallel with T015)
    ↓
T018, T019, T020 (polish — all parallel)
```

### Parallel Opportunities

- T002, T003 can run in parallel with T001
- T005, T006 can run in parallel (different files)
- T012 can run in parallel with T008–T011 (different files)
- T017 can run in parallel with T015–T016 (locale file only)
- T018, T019, T020 all parallel

### Implementation Strategy

**MVP (US1 only)**: Complete Phases 1–2–3 → English strings load from catalogue, all tooltips shown.
**Full feature**: Add Phase 4 (tooltip audit) → Phase 5 (Settings dialog) → Phase 6 (polish).
