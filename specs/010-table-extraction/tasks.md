# Tasks: Table Extraction

**Branch**: `010-table-extraction` | **Date**: 2026-09-19 | **Spec**: [spec.md](file:///d:/Coding/LearnSpecKit/Proj1/specs/010-table-extraction/spec.md) | **Plan**: [plan.md](file:///d:/Coding/LearnSpecKit/Proj1/specs/010-table-extraction/plan.md)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify dependencies and add shared localization strings for the new rule type.

- [X] T001 Verify Python dependencies (`PyMuPDF>=1.23.0`, `PySide6>=6.6.0`, `pydantic>=2.4.0`) in requirements.txt
- [X] T002 [P] Add i18n translation keys for Table rule type and table configuration options in src/i18n/locales/en.json and src/i18n/locales/vi.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain enums and Pydantic models required by all subsequent user stories.

**⚠️ CRITICAL**: No user story implementation can proceed until foundational domain models are complete and verified.

- [X] T003 [P] Add `TABLE = "TABLE"` to `RuleType` enum and create `TableStrategy(str, Enum)` with values `LINES = "lines"`, `TEXT = "text"`, `EXPLICIT = "explicit"` in src/domain/enums.py
- [X] T004 [P] Implement `TableConfig` and `TableExtractionRule` Pydantic models with constraints (`header_rows_count >= 0, default 1`, `snap_tolerance >= 0.0, default 3.0`, `page_index >= 0, default 0`) and update `ExtractionRule` discriminated union in src/domain/models.py
- [X] T005 Create unit tests for `TableConfig` and `TableExtractionRule` serialization, validation, and JSON schema compatibility in tests/unit/test_table_rule.py

**Checkpoint**: Foundation ready - domain models and validation pass tests. User story implementation can now begin.

---

## Phase 3: User Story 1 - Define Table Extraction Rule (Priority: P1) 🎯 MVP

**Goal**: Enable users to select "Table" as a rule type when creating rules, define table bounding boxes on the canvas, and save templates with table rules.

**Independent Test**: Create a template, add a Table rule via the rule dialog with a bounding box, save the template, and verify the persisted JSON contains `rule_type="TABLE"` and valid coordinates.

### Tests for User Story 1
> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T006 [P] [US1] Create unit tests for Table rule creation and canvas interaction in tests/unit/test_table_rule_ui.py

### Implementation for User Story 1

- [X] T007 [US1] Update `RuleDialog` in src/ui/rule_dialog.py to support `RuleType.TABLE`, initialize table box from canvas selection, and construct `TableExtractionRule` on save
- [X] T008 [US1] Update `TemplateController` in src/controllers/template_controller.py to handle `RuleType.TABLE` when adding and displaying rules in workspace
- [X] T009 [US1] Update canvas highlight rendering in src/ui/pdf_canvas.py to visually distinguish Table rules with green highlight border

**Checkpoint**: User Story 1 complete and independently testable. Templates can define and persist Table rules.

---

## Phase 4: User Story 3 - Extract and Export Table Data (Priority: P1)

**Goal**: Extract structured 2D table data from PDF files using PyMuPDF and export flattened JSON strings into the main batch CSV file.

**Independent Test**: Run batch extraction on a document containing a table rule, verify `ExtractedRecord` has 2D table list, and verify CSV output has valid JSON string in the table column.

### Tests for User Story 3
> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US3] Create unit tests for table extraction strategy with PyMuPDF in tests/unit/test_table_strategy.py
- [X] T011 [P] [US3] Create unit test for CSV exporter JSON flattening of table data in tests/unit/test_csv_exporter_table.py
- [X] T012 [P] [US3] Create integration test for batch extraction of tables in tests/integration/test_batch_table_extraction.py

### Implementation for User Story 3

- [X] T013 [US3] Implement `TableExtractionStrategy` inheriting `IExtractionStrategy` using `page.find_tables(clip=...)` returning 2D list of extracted cell strings in src/strategies/table_strategy.py
- [X] T014 [US3] Register `TableExtractionRule` in `ExtractionStrategyFactory.create()` in src/strategies/factory.py
- [X] T015 [US3] Update `process_file_worker` in src/services/batch_engine.py to route `TableExtractionRule` extraction with its `page_index`
- [X] T016 [US3] Update `CSVExporter.export()` in src/services/csv_exporter.py to serialize list/dict extracted values as JSON strings using `json.dumps(val, ensure_ascii=False)`

**Checkpoint**: User Story 3 complete. Batch processing successfully extracts table rows/columns and exports them into CSV.

---

## Phase 5: User Story 2 - Advanced Table Configuration (Priority: P2)

**Goal**: Provide advanced configuration controls (borderless/bordered, vertical/horizontal strategies, header rows count, snap tolerance) and ensure the extraction engine respects these options.

**Independent Test**: Configure advanced table settings in rule dialog, preview extraction against a sample PDF, and verify extraction strategy reflects custom parameters.

### Tests for User Story 2
> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T017 [P] [US2] Create unit tests for advanced table configuration parameters in extraction strategy in tests/unit/test_table_advanced_strategy.py

### Implementation for User Story 2

- [X] T018 [US2] Add advanced table configuration controls (`has_borders` checkbox, `vertical_strategy` combo, `horizontal_strategy` combo, `header_rows_count` spinbox, `snap_tolerance` spinbox) to src/ui/rule_dialog.py
- [X] T019 [US2] Pass advanced `TableConfig` options to PyMuPDF `find_tables(clip=..., strategy=..., vertical_strategy=..., horizontal_strategy=..., snap_tolerance=...)` in src/strategies/table_strategy.py
- [X] T020 [US2] Update single-rule preview in src/controllers/template_controller.py and src/ui/rule_preview_dialog.py to format and display structured table results nicely

**Checkpoint**: User Story 2 complete. Advanced table extraction options configurable from UI and applied during extraction.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end validation, sample documents, and full test suite verification.

- [X] T021 [P] Add sample test fixture PDF with bordered and borderless tables in tests/fixtures/sample_tables.pdf
- [X] T022 Run end-to-end quickstart validation scenarios per specs/010-table-extraction/quickstart.md
- [X] T023 Verify full test suite passes with `pytest tests/` and resolve any typing or lint warnings

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Story 1 (Phase 3 - P1)**: Depends on Foundational completion. Enables rule authoring.
- **User Story 3 (Phase 4 - P1)**: Depends on Foundational completion and Table rule definition. Enables extraction & export.
- **User Story 2 (Phase 5 - P2)**: Depends on User Story 1 (UI dialog) and User Story 3 (Table strategy). Adds advanced configuration tuning.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### Parallel Opportunities

- Within Phase 1: `T002` can run in parallel with `T001`.
- Within Phase 2: `T003` and `T004` can run in parallel.
- Within Phase 3 (US1): `T006` tests can be written while reviewing UI components.
- Within Phase 4 (US3): `T010`, `T011`, and `T012` tests can be written in parallel.
- Within Phase 5 (US2): `T017` tests can be written in parallel with UI setup.

---

## Parallel Example: User Story 3

```bash
# Launch test creation for User Story 3 in parallel:
Task: "Create unit tests for table extraction strategy with PyMuPDF in tests/unit/test_table_strategy.py"
Task: "Create unit test for CSV exporter JSON flattening of table data in tests/unit/test_csv_exporter_table.py"
Task: "Create integration test for batch extraction of tables in tests/integration/test_batch_table_extraction.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup (`T001`, `T002`)
2. Complete Phase 2: Foundational (`T003`, `T004`, `T005`)
3. Complete Phase 3: User Story 1 (`T006`, `T007`, `T008`, `T009`)
4. **STOP and VALIDATE**: Verify Table rule can be created on canvas and saved in template.

### Incremental Delivery
1. Setup + Foundational -> Domain ready
2. Add User Story 1 (P1) -> Test independently -> Rule authoring MVP
3. Add User Story 3 (P1) -> Test independently -> Full extraction & CSV export pipeline
4. Add User Story 2 (P2) -> Test independently -> Advanced configuration controls
5. Run Polish & Quickstart validation
