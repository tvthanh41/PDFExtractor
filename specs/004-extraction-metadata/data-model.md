# Data Model: Extraction Metadata

No structural changes are made to the persistent `Template` model or `ExtractionRule` classes.

## In-Memory Enhancements

The output dictionary presented to the UI and CSV exporter will be augmented with standard keys:

- `file name` (string)
- `file path` (string)
- `generated time` (string, ISO-like format)
- `user` (string)
- `template name` (string)

The `ExtractedRecord` class inside `batch_engine.py` will not be altered, but `CSVExporter` will dynamically pull the timestamp, user, and template name during the write operation.
