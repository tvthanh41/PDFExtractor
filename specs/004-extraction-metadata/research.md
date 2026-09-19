# Research: Extraction Metadata

## Fetching System Data
- **File Name / Path**: Already available in `TemplateController.current_pdf_path` and `ExtractedRecord`.
- **Generated Time**: Use `datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")`.
- **User**: Use `getpass.getuser()`. 
  - *Risk*: `getpass` can throw an exception if the user name cannot be found in the environment.
  - *Mitigation*: Wrap in a `try...except` block and default to `"Unknown"`.
- **Template Name**: Available via `self.template.name`.

## Existing Output Hooks
- **Preview Output**: Generated inside `TemplateController.preview_extraction()` as a standard Python dictionary `results = {}`. We can just append to this dictionary.
- **Batch Export**: `CSVExporter` already manages standard columns `["_file_name", "_file_path", "_status", "_error_message"]`. We will modify these headers to exactly match the spec request. The spec asks for "file name", "file path", "generated time", "user", "template name" (so we will rename `_file_name` to `file name` for consistency, or keep the underscore format and add the new ones, let's just use exact strings the user requested for clarity).
