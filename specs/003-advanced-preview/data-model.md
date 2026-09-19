# Data Model: Advanced Preview

No changes to the persistent data model (`AnchorExtractionRule`, `BoundingBoxExtractionRule`, etc.) are required for this feature. 

The feature purely affects the transient UI layer and does not alter how templates are stored in `.pdftpl` files.

## UI Data Structures

While no persistent data model changes are required, the UI components will pass data using standard Python structures:

### Preview Dialog Data Contract
- **Input**: `dict[str, str]` 
  - Represents the fully extracted data from the PDF.
  - Keys are rule `key_name`s, values are the extracted strings.

### Single Rule Preview Contract
- **Input**: `key_name: str`, `extracted_text: str`
  - Represents the targeted extraction for a single executed rule.
