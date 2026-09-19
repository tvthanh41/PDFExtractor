# Tasks: Advanced Rule Configuration

**Feature**: 006-advanced-rule-config
**Branch**: `006-featurename-006-advanced`

---

## Phase 1: Setup

*No new infrastructure needed — modifying existing UI file only.*

- [X] T001 Verify `src/ui/rule_dialog.py` structure and identify exact insertion points for advanced sections
---

## Phase 2: Foundational

*No blocking prerequisites — changes are isolated to one UI file.*

---

## Phase 3: User Story 1 — Anchor Rule Advanced Settings (Priority: P1) 🎯 MVP

**Goal**: Expose `offset_distance` and `match_index` in a collapsible Advanced Settings section of the Anchor rule form.

**Independent Test**: Create an anchor rule, set offset_distance=300 and match_index=1, save and re-open — values must persist. Create another without touching Advanced Settings — defaults (150.0, 0) must be used.

### Implementation

- [X] T002 [US1] Add `offset_distance` QDoubleSpinBox (min=0, max=9999, step=10, default=150.0) and `match_index` QSpinBox (min=0, max=99, default=0) inside a hidden `QGroupBox` in the anchor section of `src/ui/rule_dialog.py`
- [X] T003 [US1] Add toggle `QPushButton("▶ Advanced Settings")` to anchor section that shows/hides the QGroupBox and updates its label to `▼ Advanced Settings` in `src/ui/rule_dialog.py`
- [X] T004 [US1] Update `_create_rule()` in `src/ui/rule_dialog.py` to read `offset_distance` and `match_index` from the spinners instead of using Pydantic defaults
- [X] T005 [US1] Update `_populate(rule)` in `src/ui/rule_dialog.py` to pre-fill `offset_distance` and `match_index` spinners when editing an existing anchor rule
- [X] T006 [P] [US1] Add unit tests for anchor advanced settings round-trip in `tests/unit/test_rule_dialog_advanced.py`

**Checkpoint**: Anchor rule advanced settings fully functional and tested.

---

## Phase 4: User Story 2 — Bounding Box `page_index` Setting (Priority: P2)

**Goal**: Expose `page_index` in a collapsible Advanced Settings section of the Bounding Box rule form, replacing the hardcoded `page_index=0`.

**Independent Test**: Create a bounding box rule, set page_index=2, save and re-open — value must persist. Check `.pdftpl` JSON contains `"page_index": 2`.

### Implementation

- [X] T007 [US2] Add `page_index` QSpinBox (min=0, max=999, default=0) inside a hidden `QGroupBox` in the bounding box section of `src/ui/rule_dialog.py`
- [X] T008 [US2] Add toggle `QPushButton("▶ Advanced Settings")` to bounding box section that shows/hides the QGroupBox in `src/ui/rule_dialog.py`
- [X] T009 [US2] Update `_create_rule()` in `src/ui/rule_dialog.py` to read `page_index` from the spinner (replacing the hardcoded `page_index=0`)
- [X] T010 [US2] Update `_populate(rule)` in `src/ui/rule_dialog.py` to pre-fill `page_index` spinner when editing an existing bounding box rule
- [X] T011 [P] [US2] Add unit tests for bounding box page_index round-trip in `tests/unit/test_rule_dialog_advanced.py`

**Checkpoint**: Bounding box page_index fully functional and tested.

---

## Phase 5: Polish & Cross-Cutting Concerns

- [X] T012 Run full test suite: `uv run pytest tests/ -v` — 27 passed
- [X] T013 Run quickstart.md validation scenarios manually


---

## Dependencies & Execution Order

- T001 → T002 → T003 → T004 → T005 (sequential, same file)
- T006 can run in parallel with T002–T005 (different file)
- T007–T011 depend on T001 but are independent of T002–T006
- T012–T013 depend on all prior tasks

### Parallel Opportunities

- US1 and US2 touch the same file (`rule_dialog.py`), so they should be done **sequentially** to avoid conflicts.
- Test files for US1 (T006) and US2 (T011) can be written in parallel with implementation.
