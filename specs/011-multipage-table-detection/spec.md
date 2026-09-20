# Feature Specification: Multi-Page Navigation and Pattern-Based Table Detection

**Feature Branch**: `011-multipage-table-detection`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "Currently the pdf file opened in the GUI only show first page, we need it show all page and we should include the current page index in the method that we extract the data for each method. Next, we need to add an option so that it can automatically detect the position of the table. For example we can allow user enter a pattern for start of table and a pattern for end of table (they should be allow to choose include or exlclude the start and end separately). This method also should work for anchor text, we need to automatically read the document and find the relevant information, incase have many example return, we can allow user skip first k result and pick the top 1 from the rest for example. We need to review that very carefully to not make spaghetti code base. Next, we need to extend the functionality by using PyMuPDF4LLM. Current code base work well, but that library can make our work better, so try to add that library is good idea."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-Page Viewing and Page-Aware Rule Creation (Priority: P1)

As a user opening multi-page PDF documents, I want to navigate through all pages of the document in the GUI workspace, view the current page number and total pages, and have any extraction rule automatically record the current active page index so that rules can target data located on any page in the document.

**Why this priority**: Currently the application only displays the first page, preventing users from viewing or configuring extraction rules for any data on subsequent pages. This is the prerequisite foundation for all multi-page document workflows.

**Independent Test**: Load a 5-page PDF into the application. Navigate between pages 1 through 5 using pagination controls. Create an extraction rule on page 3. Verify that the rule captures `page_index: 2` and extracts data correctly from page 3 during single and batch extraction.

**Acceptance Scenarios**:

1. **Given** a multi-page PDF loaded in the workspace, **When** the user clicks "Next Page" or inputs a specific page number, **Then** the canvas updates immediately to render the requested page with correct scaling and active highlights.
2. **Given** the user is viewing page 3 of a document, **When** the user creates a new extraction rule (bounding box, anchor text, or table), **Then** the rule dialog defaults its page index to 2 (0-indexed) or displays page 3 (1-indexed for the user).
3. **Given** an extraction rule defined on page 2, **When** batch extraction runs, **Then** the extractor extracts content from page 2 rather than page 0.

---

### User Story 2 - Pattern-Based Dynamic Table Detection (Priority: P1)

As a user extracting structured table data whose vertical position or height varies across different documents, I want to define a table extraction rule using start and end text patterns with optional inclusion/exclusion toggles, so that the application dynamically detects the table's bounding area on the document.

**Why this priority**: Static bounding box coordinates fail when invoices or reports have variable numbers of line items, causing tables to shift vertically or change size. Automatic boundary detection ensures reliable extraction across variable layouts.

**Independent Test**: Configure a table extraction rule with a start pattern (e.g. `Item Description`) and end pattern (e.g. `Subtotal`), with start included and end excluded. Run extraction on documents where the table appears at different vertical coordinates. Verify that the table bounding box is dynamically computed and line items are extracted accurately.

**Acceptance Scenarios**:

1. **Given** a table rule configured with start pattern "Header A" (included) and end pattern "Total" (excluded), **When** extraction executes, **Then** the extractor locates "Header A" as the top boundary (including the header line) and "Total" as the bottom boundary (excluding the total line), extracting the tabular area between them.
2. **Given** a document where the start pattern appears multiple times, **When** extraction executes, **Then** the system utilizes occurrence selection parameters (e.g. skip first $k$ matches and select the desired instance) to accurately locate the intended table.
3. **Given** a document where the end pattern is not found following the start pattern, **When** extraction runs, **Then** the system follows the configured fallback behavior (e.g. bounded to the bottom margin of the page or reporting a clear boundary error) without crashing.

---

### User Story 3 - Anchor Text Search with Occurrence Offset Selection (Priority: P2)

As a user extracting key-value data where the anchor label appears multiple times in a document (e.g. repeated "Date:" or "Total:"), I want to configure the anchor search rule to skip the first $k$ occurrences and pick a specific occurrence, so that I can reliably extract values associated with repeated labels.

**Why this priority**: Real-world forms and financial statements frequently repeat identical field names across headers, summary blocks, and itemized sections. Being able to skip $k$ matches provides robust targeting.

**Independent Test**: Load a PDF containing three occurrences of "Total:". Define an anchor rule for "Total:" with `skip_k: 2` (or match index 2) to target the 3rd occurrence. Verify that the extracted value matches the text directly adjacent to the 3rd "Total:" label.

**Acceptance Scenarios**:

1. **Given** a document with 4 occurrences of "Date:", **When** an anchor rule configured with `skip: 1` executes, **Then** the first occurrence is ignored and extraction reads adjacent text from the 2nd occurrence.
2. **Given** a document with fewer matches than $k + 1$, **When** extraction executes, **Then** the system gracefully records an empty/failed extraction for that rule with a descriptive message rather than halting execution.

---

### User Story 4 - Enhanced Structured Extraction via Layout-Aware Markdown Engine (Priority: P2)

As a user extracting complex or borderless tables and formatted sections, I want an enhanced extraction strategy leveraging PyMuPDF4LLM layout parsing, so that multi-column tables, headers, and text formatting are accurately extracted into clean tabular data and structured markdown.

**Why this priority**: Standard line-based table extraction can struggle with borderless or multi-line cell layouts. PyMuPDF4LLM provides advanced layout heuristic reconstruction, significantly improving extraction quality for complex documents.

**Independent Test**: Select the "PyMuPDF4LLM / Layout Markdown" strategy on a borderless financial table. Verify that table headers, columns, and rows are correctly parsed into structured table records without cell misalignment.

**Acceptance Scenarios**:

1. **Given** a PDF with borderless tables or complex text flow, **When** the layout-aware extraction method is executed on a selected page or region, **Then** it generates clean structured tabular/markdown records.
2. **Given** the strategy registry in the application, **When** the new engine is invoked, **Then** it adheres strictly to the existing Strategy interface, ensuring zero tight coupling and preventing architectural regressions.

---

### Edge Cases

- **Page index out of bounds**: When a rule specifies page 4 on a 2-page document during batch processing, the extractor marks the record as failed with `Page index 4 exceeds document page count (2)` without interrupting the batch job.
- **Overlapping or inverted start/end patterns**: When the end pattern is detected vertically above or preceding the start pattern, the system rejects the invalid boundary and logs an informative validation error.
- **Zero matches for patterns**: When start pattern or anchor text returns 0 matches on the document, the extraction status is set to `EMPTY` with an appropriate warning.
- **Skip count exceeding match count**: When `skip_k` is 3 but only 2 instances of the pattern exist, the rule returns `None`/empty with a descriptive log.
- **Multi-page continuous tables**: When a start pattern appears on page 1 and the end pattern appears on page 2, the behavior is handled according to page-scope constraints (bounded within page or explicitly marked cross-page).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The UI viewer MUST support navigating through all pages of a loaded PDF document using navigation controls (Previous, Next, page number input, and total page counter).
- **FR-002**: The UI canvas MUST dynamically render the selected page with appropriate scaling, maintaining pan and zoom capabilities across all pages.
- **FR-003**: All extraction rules (Anchor Search, Bounding Box, and Table) MUST include a `page_index` attribute (0-indexed internally, 1-indexed in UI presentation).
- **FR-004**: When creating or editing a rule in the GUI, the rule dialog MUST default the `page_index` to the currently active page in the viewer.
- **FR-005**: The system MUST support pattern-based dynamic table boundary detection using a configurable `start_pattern` and `end_pattern` (supporting literal text or regular expressions).
- **FR-006**: The table pattern boundary rule MUST allow the user to independently specify whether to include or exclude the start boundary row (`include_start: bool`) and end boundary row (`include_end: bool`).
- **FR-007**: The table pattern boundary rule and anchor search rule MUST allow specifying occurrence filtering (skip first $k$ results and pick the target match from remaining candidates).
- **FR-008**: The extraction engine MUST include an enhanced layout-aware extraction strategy integrating `pymupdf4llm` to extract structured tables and markdown content.
- **FR-009**: The new extraction strategies MUST adhere strictly to the existing decoupled `ExtractionStrategy` interface, ensuring headless batch processing remains independent of the UI layer.
- **FR-010**: The preview pane and test run modal MUST display extracted results for multi-page rules and pattern-based table extractions accurately.

### Key Entities *(include if feature involves data)*

- **PageNavigationState**: Represents the viewer's current active page, total pages count, and zoom/view parameters.
- **PatternBoundaryConfig**: Configuration for dynamic region detection containing `start_pattern`, `end_pattern`, `include_start` (boolean), `include_end` (boolean), `is_regex` (boolean), and `occurrence_index` / `skip_k` (integer).
- **OccurrenceFilter**: Model defining match filtering logic (`skip_k`: non-negative integer, `select_index`: non-negative integer).
- **TableExtractionRule**: Extended model containing `page_index`, optional `box` (for static coordinates), optional `pattern_boundary` (for dynamic detection), and table parsing configuration.
- **AnchorExtractionRule**: Extended model containing `page_index`, `anchor_text`, `search_mode`, `direction`, `offset_distance`, and `skip_k` / `match_index`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can view and navigate to any page of a 100-page PDF in under 1 second per page transition.
- **SC-002**: Users can successfully define and execute extraction rules targeting any arbitrary page in a multi-page document with 100% rule-to-page fidelity.
- **SC-003**: Dynamic table boundary detection accurately isolates variable-height tables on 95% of test documents where vertical positions shift across files.
- **SC-004**: Anchor and pattern occurrence filtering allows targeting specific repeated labels (e.g. 2nd or 3rd match) with 100% deterministic accuracy.
- **SC-005**: Extraction logic remains 100% decoupled from PySide6 UI components, with automated test suite coverage passing across all new strategies and domain models.

## Assumptions

- **Navigation UI Layout**: Page navigation controls (Previous button, Next button, current page spinbox/input, and total pages label) will be placed directly above or below the PDF canvas within the workspace tab.
- **Page Index Scope**: For pattern-based table detection, the primary search scope is within the specified `page_index` by default; cross-page table continuation will treat the table within the specified page unless multi-page span is explicitly configured.
- **Pattern Matching Format**: Pattern inputs support both standard text substring matching and optional regular expressions.
- **PyMuPDF4LLM Installation**: `pymupdf4llm` is added to `requirements.txt` as a runtime dependency.
- **Backward Compatibility**: Existing saved templates with `BoundingBoxExtractionRule` and `TableExtractionRule` will load seamlessly without schema validation errors.
