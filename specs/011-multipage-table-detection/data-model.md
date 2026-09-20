# Data Model: Multi-Page Navigation and Pattern-Based Table Detection

## Domain Enums

### `TableBoundaryType` (New Enum)
Determines how the boundary coordinates of a table are defined.
- `BOUNDING_BOX` = `"BOUNDING_BOX"` (fixed percentage coordinates)
- `PATTERN_MATCH` = `"PATTERN_MATCH"` (dynamic start and end pattern matching)

### `TableEngine` (New Enum)
Selects the underlying extraction engine for tabular data.
- `PYMUPDF` = `"pymupdf"` (native `Page.find_tables()`)
- `PYMUPDF4LLM` = `"pymupdf4llm"` (layout-aware markdown table reconstruction)

---

## Domain Models

### `PatternBoundaryConfig` (Pydantic Model)
Represents configuration for dynamic table region detection via text/regex markers.

| Field Name | Type | Validation / Default | Description |
|---|---|---|---|
| `start_pattern` | `str` | non-empty | Text or regex identifying the start of the table. |
| `end_pattern` | `str` | non-empty | Text or regex identifying the end of the table. |
| `include_start` | `bool` | Default: `True` | Whether the matching start line is included in the table. |
| `include_end` | `bool` | Default: `False` | Whether the matching end line is included in the table. |
| `is_regex` | `bool` | Default: `False` | Whether `start_pattern` and `end_pattern` are regular expressions. |
| `skip_k` | `int` | `>= 0`, Default: `0` | Number of start pattern occurrences to skip before selecting the target. |

### `TableConfig` (Pydantic Model - Updated)
Extended with engine selection.

| Field Name | Type | Validation / Default | Description |
|---|---|---|---|
| `has_borders` | `bool` | Default: `True` | Whether table has visible boundary lines. |
| `vertical_strategy` | `TableStrategy` | Default: `LINES` | Strategy for column detection in PyMuPDF. |
| `horizontal_strategy` | `TableStrategy` | Default: `LINES` | Strategy for row detection in PyMuPDF. |
| `header_rows_count` | `int` | `>= 0`, Default: `1` | Number of header rows. |
| `snap_tolerance` | `float` | `>= 0.0`, Default: `3.0` | Distance tolerance for snapping text into cells. |
| `extract_as_key_value` | `bool` | Default: `False` | Whether to extract table as key-value pairs (`Dict[str, str]`). |
| `engine` | `TableEngine` | Default: `PYMUPDF` | Extraction engine: PyMuPDF or PyMuPDF4LLM. |

### `TableExtractionRule` (Pydantic Model - Updated)
Extended to support both fixed bounding boxes and dynamic pattern boundaries.

| Field Name | Type | Validation / Default | Description |
|---|---|---|---|
| `rule_id` | `str` | Default UUID | Unique rule ID. |
| `key_name` | `str` | non-empty | Output key name for extracted table. |
| `data_type` | `DataType` | `DataType.STRING` | Data type classification. |
| `rule_type` | `RuleType` | Constant: `TABLE` | Rule type identifier. |
| `page_index` | `int` | `>= 0`, Default: `0` | Zero-indexed PDF page. |
| `boundary_type` | `TableBoundaryType` | Default: `BOUNDING_BOX` | Boundary definition method. |
| `box` | `Optional[BoundingBox]` | Optional | Static coordinates (required if `boundary_type == BOUNDING_BOX`). |
| `pattern_boundary` | `Optional[PatternBoundaryConfig]` | Optional | Pattern configuration (required if `boundary_type == PATTERN_MATCH`). |
| `config` | `TableConfig` | Default `TableConfig()` | Advanced table parsing settings. |

### `AnchorExtractionRule` (Pydantic Model - Updated)
Explicitly includes `page_index`.

| Field Name | Type | Validation / Default | Description |
|---|---|---|---|
| `rule_id` | `str` | Default UUID | Unique rule ID. |
| `key_name` | `str` | non-empty | Output key name. |
| `data_type` | `DataType` | `DataType.STRING` | Data type classification. |
| `rule_type` | `RuleType` | Constant: `ANCHOR_SEARCH` | Rule type identifier. |
| `page_index` | `int` | `>= 0`, Default: `0` | Zero-indexed PDF page to search. |
| `anchor_text` | `str` | non-empty | Search string or regex. |
| `search_mode` | `SearchMode` | Default: `EXACT` | Exact, contains, regex, case-insensitive. |
| `direction` | `Direction` | Default: `RIGHT` | Search direction for target value. |
| `offset_distance` | `float` | `>= 0`, Default: `150.0` | Search bounding distance in points. |
| `match_index` | `int` | `>= 0`, Default: `0` | Occurrence index (equivalent to `skip_k`). |

---

## State Model: GUI Canvas Navigation

### `PageNavigationState`
Managed by `PdfCanvasWidget` and synchronized with `WorkspaceTab`:
- `current_page: int` (0-indexed, internally tracked)
- `total_pages: int` (total pages in current `fitz.Document`)
- `can_navigate_prev: bool` (`current_page > 0`)
- `can_navigate_next: bool` (`current_page < total_pages - 1`)
