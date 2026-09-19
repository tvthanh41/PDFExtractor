# Data Model & Contracts

## New Entities

### `Translator` (`src/i18n/translator.py`)

```python
class Translator:
    def __init__(self):
        self._active: dict[str, str] = {}   # selected locale
        self._fallback: dict[str, str] = {}  # always en.json

    def load(self, locale_data: dict, fallback_data: dict) -> None: ...
    def translate(self, key: str) -> str:
        # 1. active locale
        # 2. fallback (English)
        # 3. return key itself
        ...

# Module-level singleton + convenience function
translator = Translator()
def t(key: str) -> str:
    return translator.translate(key)
```

### `LocaleLoader` (`src/i18n/locale_loader.py`)

```python
class LocaleLoader:
    LOCALES_DIR = Path(__file__).parent / "locales"

    @classmethod
    def discover(cls) -> dict[str, str]:
        """Returns {language_code: display_name} from scanning *.json files."""

    @classmethod
    def load(cls, language_code: str) -> dict:
        """Loads and returns the dict for the given language code."""
```

### `PreferencesService` (`src/services/preferences_service.py`)

```python
class PreferencesService:
    PREFS_PATH = Path.home() / ".pdftpl_prefs.json"

    @classmethod
    def get(cls, key: str, default=None): ...
    @classmethod
    def set(cls, key: str, value) -> None: ...
    @classmethod
    def get_language(cls) -> str: ...       # returns "en" if not set
    @classmethod
    def set_language(cls, code: str) -> None: ...
```

---

## Locale File Contract (`src/i18n/locales/en.json`)

Flat JSON. Required keys:

| Key | Value |
|-----|-------|
| `_meta.language_name` | `"English"` |
| **Main Window** | |
| `menu.file` | `"File"` |
| `menu.file.new_template` | `"New Template"` |
| `menu.file.open_template` | `"Open Template..."` |
| `menu.file.run_batch` | `"Run Batch Extraction..."` |
| `menu.edit.settings` | `"Settings..."` |
| `menu.edit` | `"Edit"` |
| `window.title` | `"PDF Data Extractor"` |
| **Workspace Tab** | |
| `btn.open_pdf` | `"Open PDF"` |
| `btn.add_rule` | `"Add Rule"` |
| `btn.add_box_rule` | `"Add Box Rule"` |
| `btn.save_template` | `"Save Template"` |
| `btn.preview_extraction` | `"Preview Extraction"` |
| `btn.preview` | `"Preview"` |
| `table.col.key` | `"Key"` |
| `table.col.type` | `"Type"` |
| `table.col.rule_type` | `"Rule Type"` |
| `table.col.actions` | `"Actions"` |
| `label.preview` | `"Preview: None"` |
| **Tooltips — Workspace** | |
| `tooltip.btn.open_pdf` | `"Load a PDF file to view and extract data from."` |
| `tooltip.btn.add_rule` | `"Add an anchor-based extraction rule that finds a value relative to a text label."` |
| `tooltip.btn.add_box_rule` | `"Draw a bounding box on the canvas to define a fixed extraction region."` |
| `tooltip.btn.save_template` | `"Save the current template with all its rules to a .pdftpl file."` |
| `tooltip.btn.preview_extraction` | `"Run all rules against the loaded PDF and preview the extracted values."` |
| `tooltip.btn.preview_rule` | `"Preview the extraction result for this specific rule."` |
| **Rule Dialog** | |
| `rule_dialog.title.create` | `"Create Extraction Rule"` |
| `rule_dialog.title.edit` | `"Edit Extraction Rule"` |
| `rule_dialog.label.key_name` | `"Key Name:"` |
| `rule_dialog.label.data_type` | `"Data Type:"` |
| `rule_dialog.label.rule_type` | `"Rule Type:"` |
| `rule_dialog.label.anchor_text` | `"Anchor Text:"` |
| `rule_dialog.label.search_mode` | `"Search Mode:"` |
| `rule_dialog.label.direction` | `"Direction:"` |
| `rule_dialog.label.advanced` | `"▶  Advanced Settings"` |
| `rule_dialog.label.advanced_open` | `"▼  Advanced Settings"` |
| `rule_dialog.label.offset_distance` | `"Offset Distance (px):"` |
| `rule_dialog.label.match_index` | `"Match Index:"` |
| `rule_dialog.label.page_index` | `"Page Index (0-based):"` |
| `rule_dialog.label.box_defined` | `"Bounding Box defined from canvas."` |
| `rule_dialog.label.box_undefined` | `"Please define bounding box on canvas."` |
| `btn.save` | `"Save"` |
| `btn.cancel` | `"Cancel"` |
| **Tooltips — Rule Dialog** | |
| `tooltip.rule_dialog.key_name` | `"The output column name for this extracted value. Use lowercase with underscores (e.g. total_amount)."` |
| `tooltip.rule_dialog.data_type` | `"The expected data type of the extracted value."` |
| `tooltip.rule_dialog.rule_type` | `"How the extraction region is defined: by anchor text or by a fixed bounding box."` |
| `tooltip.rule_dialog.anchor_text` | `"The text label to search for on the page. The value will be extracted relative to this label."` |
| `tooltip.rule_dialog.search_mode` | `"How to match the anchor text: exact match, substring, regex, or case-insensitive."` |
| `tooltip.rule_dialog.direction` | `"Where to look for the value relative to the anchor text."` |
| `tooltip.rule_dialog.offset_distance` | `"Maximum pixel distance from the anchor to search for a value. Increase if the value is far from the label."` |
| `tooltip.rule_dialog.match_index` | `"Which occurrence of the anchor text to use. 0 = first, 1 = second, etc."` |
| `tooltip.rule_dialog.page_index` | `"Which page to extract from (0-based). 0 = first page."` |
| **Batch Config Dialog** | |
| `batch_dialog.title` | `"Batch Extraction"` |
| `batch_dialog.heading` | `"Configure Batch Extraction"` |
| `batch_dialog.subtitle` | `"Select the template file, input PDF folder, and output CSV path, then click Start Batch."` |
| `batch_dialog.label.template` | `"Template File (.pdftpl):"` |
| `batch_dialog.label.input_dir` | `"Input PDF Folder:"` |
| `batch_dialog.label.output_csv` | `"Output CSV File:"` |
| `btn.browse` | `"Browse..."` |
| `btn.save_as` | `"Save As..."` |
| `btn.start_batch` | `"Start Batch"` |
| `tooltip.batch_dialog.template` | `"The extraction template (.pdftpl) defining the rules to apply."` |
| `tooltip.batch_dialog.input_dir` | `"Folder containing the PDF files to process."` |
| `tooltip.batch_dialog.output_csv` | `"Path where the results CSV will be saved."` |
| **Settings Dialog** | |
| `settings.title` | `"Settings"` |
| `settings.label.language` | `"Language:"` |
| `settings.info.restart` | `"Please restart the application to apply the new language."` |
| `tooltip.settings.language` | `"Select the display language. A restart is required to apply the change."` |
| **Common** | |
| `btn.ok` | `"OK"` |
| `msg.error` | `"Error"` |
| `msg.info` | `"Info"` |

---

## Settings Dialog Contract (`src/ui/settings_dialog.py`) [NEW]

```python
class SettingsDialog(QDialog):
    def __init__(self, preferences: PreferencesService, available_languages: dict, parent=None): ...
    # Shows: language dropdown (populated from available_languages)
    # On OK: saves preference via preferences.set_language(code)
    #        shows info message about restart
```
