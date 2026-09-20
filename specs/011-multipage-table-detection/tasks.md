# Tasks: Multi-Page Navigation and Pattern-Based Table Detection

**Feature**: Multi-Page Navigation and Pattern-Based Table Detection  
**Spec**: [spec.md](file:///d:/Coding/LearnSpecKit/Proj1/specs/011-multipage-table-detection/spec.md) | **Plan**: [plan.md](file:///d:/Coding/LearnSpecKit/Proj1/specs/011-multipage-table-detection/plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Dependency installation and baseline verification

- [X] T001 Add `pymupdf4llm>=0.0.17` to `requirements.txt`
- [X] T002 Install updated dependencies including `pymupdf4llm` into the virtual environment using `.venv\Scripts\pip install -r requirements.txt`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain enums and Pydantic models required across all user stories

- [X] T003 [P] Add `TableBoundaryType` (`BOUNDING_BOX = "BOUNDING_BOX"`, `PATTERN_MATCH = "PATTERN_MATCH"`) and `TableEngine` (`PYMUPDF = "pymupdf"`, `PYMUPDF4LLM = "pymupdf4llm"`) enums in `src/domain/enums.py`
- [X] T004 [P] Define `PatternBoundaryConfig` model in `src/domain/models.py` with fields: `start_pattern: str` (non-empty), `end_pattern: str` (non-empty), `include_start: bool = True`, `include_end: bool = False`, `is_regex: bool = False`, and `skip_k: int = Field(default=0, ge=0)`
- [X] T005 Update `TableConfig` in `src/domain/models.py` to add `engine: TableEngine = TableEngine.PYMUPDF`
- [X] T006 Update `AnchorExtractionRule` in `src/domain/models.py` to add `page_index: int = Field(default=0, ge=0)`
- [X] T007 Update `TableExtractionRule` in `src/domain/models.py` to support `boundary_type: TableBoundaryType = TableBoundaryType.BOUNDING_BOX`, `box: Optional[BoundingBox] = None`, and `pattern_boundary: Optional[PatternBoundaryConfig] = None` with Pydantic validation
- [X] T008 [P] Add unit tests validating Pydantic serialization and backwards compatibility for updated rule models in `tests/unit/test_multipage_models.py`

**Checkpoint**: Core domain models verified - User story implementation can now proceed in parallel.

---

## Phase 3: User Story 1 - Multi-Page Viewing and Page-Aware Rule Creation (Priority: P1) 🎯 MVP

**Goal**: Enable navigation across all PDF pages in the viewer canvas, display current/total pages, and ensure extraction rules capture and execute on the designated `page_index`.

**Independent Test**: Open a 3+ page PDF. Use previous/next buttons and page spinbox to view page 2. Create a rule on page 2. Verify `page_index == 1` is saved, and batch/preview extraction reads from page 2.

### Tests for User Story 1

- [X] T009 [P] [US1] Create unit tests for canvas multi-page state transitions, next/prev navigation, and page boundary clamping in `tests/unit/test_multipage_canvas.py`
- [X] T010 [P] [US1] Create unit tests verifying rule execution with distinct `page_index` values across documents in `tests/unit/test_page_index_execution.py`

### Implementation for User Story 1

- [X] T011 [US1] Extend `PdfCanvasWidget` in `src/ui/pdf_canvas.py` with `total_pages: int`, `set_page(page_index: int)`, `next_page()`, `prev_page()`, and `page_changed = Signal(int, int)`
- [X] T012 [US1] Add page navigation toolbar (Previous button, Next button, `QSpinBox` 1-indexed, and total page label) to `WorkspaceTab` in `src/ui/workspace_tab.py`
- [X] T013 [US1] Connect canvas `page_changed` signal and toolbar buttons to `TemplateController` in `src/controllers/template_controller.py`
- [X] T014 [US1] Update `RuleDialog` in `src/ui/rule_dialog.py` to display and edit `page_index` (1-indexed display, 0-indexed internal), defaulting to the canvas current viewing page
- [X] T015 [US1] Update `TemplateController.preview_extraction` and `test_rule_extraction` in `src/controllers/template_controller.py` to pass `rule.page_index` to strategy extraction instead of hardcoding canvas active page
- [X] T016 [US1] Update `process_file_worker` in `src/services/batch_engine.py` to retrieve `page_index` from all rule types (including `AnchorExtractionRule`) and safely skip files if `page_index` exceeds document page count

**Checkpoint**: User Story 1 complete and testable independently.

---

## Phase 4: User Story 2 - Pattern-Based Dynamic Table Detection (Priority: P1)

**Goal**: Automatically detect table vertical positions using start pattern, end pattern, include/exclude toggles, and occurrence skip count (`skip_k`).

**Independent Test**: Run extraction on a PDF with a shifting table using a start pattern (e.g. `Item Description`) and end pattern (e.g. `Subtotal`). Verify bounding coordinates are dynamically computed and rows are accurately extracted.

### Tests for User Story 2

- [X] T017 [P] [US2] Create unit tests for `BoundaryDetector` verifying start/end text matching, regex patterns, include/exclude boundary coordinates, and `skip_k` logic in `tests/unit/test_boundary_detector.py`
- [X] T018 [P] [US2] Create unit tests for dynamic pattern-based table extraction in `tests/unit/test_pattern_table_strategy.py`

### Implementation for User Story 2

- [X] T019 [US2] Create headless `BoundaryDetector` service in `src/services/boundary_detector.py` to scan `fitz.Page`, find start and end pattern matches, apply `skip_k`, and calculate the dynamic bounding rectangle `fitz.Rect`
- [X] T020 [US2] Update `TableExtractionStrategy` in `src/strategies/table_strategy.py` to use `BoundaryDetector.detect_table_bounds` when `rule.boundary_type == TableBoundaryType.PATTERN_MATCH`
- [X] T021 [US2] Update `RuleDialog` in `src/ui/rule_dialog.py` to add a "Boundary Mode" selector (`Bounding Box` vs `Pattern Match`) and UI inputs for `start_pattern`, `end_pattern`, `include_start` (checkbox), `include_end` (checkbox), `is_regex` (checkbox), and `skip_k` (spinbox)
- [X] T022 [US2] Update `WorkspaceTab.add_rule_to_table` and `update_rule_in_table` in `src/ui/workspace_tab.py` to display boundary mode summary in the rules table

**Checkpoint**: User Story 2 complete and testable independently.

---

## Phase 5: User Story 3 - Anchor Text Search with Occurrence Offset Selection (Priority: P2)

**Goal**: Enable anchor rules to skip the first $k$ matches and select a specific occurrence on the specified page.

**Independent Test**: Target a document with 3 repeated "Date:" labels on page 1. Set `skip_k = 1` (select 2nd match). Verify the extracted value is taken from the 2nd "Date:" label.

### Tests for User Story 3

- [X] T023 [P] [US3] Create unit tests in `tests/unit/test_anchor_strategy_multipage.py` verifying anchor extraction on arbitrary pages with `skip_k` occurrence selection for exact, case-insensitive, and regex modes

### Implementation for User Story 3

- [X] T024 [US3] Update `AnchorExtractionStrategy` in `src/strategies/anchor_strategy.py` to evaluate on `rule.page_index` and correctly select the $(k+1)$-th match using `rule.match_index` (`skip_k`)
- [X] T025 [US3] Update `RuleDialog` in `src/ui/rule_dialog.py` to clearly label the occurrence selection control as "Skip first k matches" / "Match Occurrence" for anchor search rules

**Checkpoint**: User Story 3 complete and testable independently.

---

## Phase 6: User Story 4 - Enhanced Structured Extraction via Layout-Aware Markdown Engine (Priority: P2)

**Goal**: Integrate `pymupdf4llm` to provide superior layout-aware structured table and markdown extraction for borderless and multi-line cell tables.

**Independent Test**: Extract a borderless table using the `PyMuPDF4LLM` engine option. Verify headers and cells align cleanly without merged text blocks.

### Tests for User Story 4

- [X] T026 [P] [US4] Create unit tests in `tests/unit/test_pymupdf4llm_table_strategy.py` verifying markdown table parsing, column normalization into `List[List[str]]`, and key-value mapping via `pymupdf4llm`

### Implementation for User Story 4

- [X] T027 [US4] Implement helper in `src/services/pdf_service.py` (or `src/strategies/table_strategy.py`) to execute `pymupdf4llm.to_markdown` on a page or clip region and parse resulting markdown tables into `List[List[str]]`
- [X] T028 [US4] Update `TableExtractionStrategy.extract` in `src/strategies/table_strategy.py` to route to the `pymupdf4llm` parser when `rule.config.engine == TableEngine.PYMUPDF4LLM`, with graceful fallback to native PyMuPDF if an error occurs
- [X] T029 [US4] Update `RuleDialog` in `src/ui/rule_dialog.py` to add an "Engine" combo box (`PyMuPDF (Native)` vs `PyMuPDF4LLM (Layout Markdown)`) under table advanced settings

**Checkpoint**: User Story 4 complete and testable independently.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Localization, end-to-end integration validation, and test suite verification

- [X] T030 [P] Add localized string entries for page navigation, pattern boundary labels, and engine selections to `src/i18n/locales/en.json` and `src/i18n/locales/vi.json`
- [X] T031 Create end-to-end integration tests in `tests/integration/test_multipage_batch.py` running a multi-page batch job with anchor, static table, pattern table, and PyMuPDF4LLM rules
- [X] T032 Run full test suite `.venv\Scripts\pytest` and verify all existing and new unit/integration tests pass with 0 errors

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - executes immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 completion - blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Phase 2 - foundational for GUI page navigation and page-index propagation.
- **User Story 2 (Phase 4)**: Depends on Phase 2 & Phase 3 (benefits from page-index propagation).
- **User Story 3 (Phase 5)**: Depends on Phase 2 & Phase 3.
- **User Story 4 (Phase 6)**: Depends on Phase 1 (pymupdf4llm dependency) & Phase 4 (table strategy extension).
- **Polish (Phase 7)**: Depends on all user story phases being complete.

### Parallel Opportunities

- All Foundational tasks marked `[P]` (T003, T004, T008) can run in parallel.
- US1 tests (T009, T010) and implementation tasks across distinct files can run in parallel.
- Boundary detector tests (T017, T018) can run alongside detector implementation (T019).
- Localization (T030) can proceed in parallel with integration testing (T031).

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (Setup) and Phase 2 (Foundational models).
2. Implement Phase 3 (User Story 1: Multi-Page Viewing & Page Indexing).
3. Validate: Open a 3-page PDF, navigate pages, create rule on page 2, verify single and batch extraction from page 2.

### Incremental Delivery

1. Deliver US1 (Multi-page navigation & page-indexed rules) -> Immediate usability fix for multi-page documents.
2. Deliver US2 (Pattern-based dynamic table detection) -> Dynamic boundary detection for variable invoices.
3. Deliver US3 (Anchor occurrence skip selection) -> Deterministic targeting for repeated labels.
4. Deliver US4 (PyMuPDF4LLM engine) -> Enhanced borderless table parsing.
5. Final polish, i18n localization, and automated regression verification.
