# Data Model: Table Extraction

## Domain Enums

### `RuleType` (Addition)
- `TABLE` = `"TABLE"`

### `TableStrategy` (New Enum)
- `LINES` = `"lines"` (detect tables using vector lines/borders)
- `TEXT` = `"text"` (detect tables using text alignment/spacing for borderless tables)
- `EXPLICIT` = `"explicit"` (detect tables using explicit grid lines)

---

## Domain Models

### `TableConfig` (Pydantic Model)
Represents advanced table parsing parameters passed to the extraction engine.

| Field Name | Type | Validation / Default | Description |
|---|---|---|---|
| `has_borders` | `bool` | Default: `True` | Whether table has visible boundary lines. |
| `vertical_strategy` | `TableStrategy` | Default: `LINES` | Strategy for detecting column boundaries. |
| `horizontal_strategy` | `TableStrategy` | Default: `LINES` | Strategy for detecting row boundaries. |
| `header_rows_count` | `int` | `>= 0`, Default: `1` | Number of top rows designated as header rows. |
| `snap_tolerance` | `float` | `>= 0.0`, Default: `3.0` | Distance tolerance for snapping text into cell grids. |
| `extract_as_key_value` | `bool` | Default: `False` | Whether to extract table as key-value pairs (Dict[str, str]). |

### `TableExtractionRule` (Pydantic Model, extends `ExtractionRuleBase`)
Represents an extraction rule targeting tabular data inside a bounding box.

| Field Name | Type | Validation / Default | Description |
|---|---|---|---|
| `rule_id` | `str` | Default UUID string | Unique identifier for rule. |
| `key_name` | `str` | non-empty | Output key name for extracted table data. |
| `data_type` | `DataType` | `DataType.STRING` | High-level data type classification. |
| `rule_type` | `RuleType` | Constant: `TABLE` | Rule type identifier for polymorphic parsing. |
| `page_index` | `int` | `>= 0`, Default: `0` | Zero-indexed page number in PDF. |
| `box` | `BoundingBox` | Required | Normalized bounding box (`x_pct`, `y_pct`, `width_pct`, `height_pct`). |
| `config` | `TableConfig` | Default `TableConfig()` | Advanced table parsing settings. |

### `ExtractionRule` (Union Update)
```python
ExtractionRule = Union[AnchorExtractionRule, BoundingBoxExtractionRule, TableExtractionRule]
```

### `ExtractedRecord` Output Structure
For a `TableExtractionRule` with `key_name="items_table"`, `extracted_values["items_table"]` holds a 2D list of strings:
```json
[
  ["Item Description", "Qty", "Price", "Total"],
  ["Widget A", "2", "$10.00", "$20.00"],
  ["Widget B", "1", "$15.00", "$15.00"]
]
```

When exported by `CSVExporter`, this 2D list is serialized into the CSV cell as:
`"[[\"Item Description\", \"Qty\", \"Price\", \"Total\"], [\"Widget A\", \"2\", \"$10.00\", \"$20.00\"], [\"Widget B\", \"1\", \"$15.00\", \"$15.00\"]]"`.
