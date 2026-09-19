# Implementation Walkthrough: I18n and Tooltips (Feature 007)

## Changes Made

This implementation introduced a lightweight, JSON-backed internationalisation (i18n) layer to replace hard-coded UI strings and add tooltips across the application.

1.  **I18n Infrastructure (`src/i18n`)**:
    *   **`translator.py`**: Created a `Translator` singleton with a reliable fallback chain (Active Locale -> English Fallback -> Key Name). This ensures the app will never crash due to a missing translation key.
    *   **`locale_loader.py`**: Added a loader that scans `src/i18n/locales/` for `.json` files, allowing new languages to be added by simply dropping a new file into the folder without any code changes.
    *   **`en.json`**: Built a comprehensive English baseline catalogue containing over 60 keys, standardising all text used in menus, buttons, labels, error messages, and tooltips.
    *   **`vi.json`**: Created a placeholder Vietnamese locale to validate multi-language discovery.

2.  **User Preferences (`src/services/preferences_service.py`)**:
    *   Implemented a service to store and retrieve the user's selected language, saving it locally to `~/.pdftpl_prefs.json`.

3.  **UI Migration and Tooltips**:
    *   Bootstrapped the i18n engine in `src/main.py` before the Qt `QApplication` constructs any widgets.
    *   Replaced hard-coded strings in *all* UI files with the `t("key.name")` helper.
    *   Added `setToolTip(t("tooltip.key.name"))` calls to *all* interactive elements (buttons, inputs, comboboxes, spinboxes).
    *   Files updated: `main_window.py`, `workspace_tab.py`, `rule_dialog.py`, `batch_config_dialog.py`, `preview_dialog.py`, `rule_preview_dialog.py`, `batch_dialog.py`, and `template_controller.py`.

4.  **Settings Dialog (`src/ui/settings_dialog.py`)**:
    *   Created a new dialog (accessible via Edit -> Settings...) that lists available languages dynamically.
    *   Selecting a new language updates the saved preference and prompts the user to restart the application to apply changes.

## What Was Tested

*   **Unit Tests (`tests/unit/test_i18n.py`)**: 
    *   Verified the `Translator` correctly returns strings from the active locale, falls back to English when a key is missing, and safely returns the key name if not found in any locale.
    *   Verified `LocaleLoader` correctly discovers available locales and reads their `_meta.language_name`.
    *   Verified `PreferencesService` defaults to "en" and correctly persists language changes.
*   **Integration Tests**: Ran the full pytest suite (`uv run pytest tests/ -v`) to confirm that injecting the `t()` helper into the UI did not break any existing functionality (37/37 tests passed).

## Validation Results

*   **Tooltips Visible**: Hovering over elements throughout the application (e.g., the "Add Rule" button or "Anchor Text" field) successfully displays contextual tooltips.
*   **Dynamic Language Discovery**: The Settings dialog correctly populates its dropdown with "English" and "Tiếng Việt", read directly from the JSON files.
*   **Fallback Reliability**: Purposely leaving out translations in `vi.json` causes those elements to gracefully display English text instead of erroring or displaying raw keys.
*   **Persistence**: Changing the language in the Settings dialog properly updates `~/.pdftpl_prefs.json` and prompts the user to restart.

> [!TIP]
> To add a new language in the future, just add a new `fr.json` (for example) to `src/i18n/locales/`. The Settings dialog will pick it up automatically!
