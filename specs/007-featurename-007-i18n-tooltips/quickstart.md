# Quickstart: UI Localisation & Tooltips

## Validation Scenario 1: Tooltips visible on all elements

1. Launch the app.
2. Hover over the **Open PDF** button in the workspace toolbar.
3. **Verify**: A tooltip appears: *"Load a PDF file to view and extract data from."*
4. Click **Add Rule**. In the dialog, hover over the **Anchor Text** field.
5. **Verify**: A tooltip appears explaining anchor text.
6. Expand **▶ Advanced Settings** and hover over **Offset Distance**.
7. **Verify**: A tooltip appears explaining pixel distance.
8. Click **Run Batch Extraction...** in the menu. Hover over the **Input PDF Folder** field.
9. **Verify**: A tooltip appears.

## Validation Scenario 2: Language setting saved and loaded

1. Open **Edit → Settings...**.
2. **Verify**: A Settings dialog appears with a **Language** dropdown defaulting to "English".
3. If a second locale file exists (e.g. `vi.json`), select it and click **OK**.
4. **Verify**: An info message appears: *"Please restart the application to apply the new language."*
5. Restart the app.
6. **Verify**: The UI now uses the selected language's strings.

## Validation Scenario 3: English fallback for missing keys

1. Create a partial locale file `src/i18n/locales/test.json` with only a few keys and `"_meta.language_name": "Test Language"`.
2. Select "Test Language" in Settings and restart.
3. **Verify**: Keys present in `test.json` show translated values; missing keys fall back to English — no crashes.

## Validation Scenario 4: Adding a new language requires no code changes

1. Create `src/i18n/locales/fr.json` with at minimum `"_meta.language_name": "Français"` and a few translated keys.
2. Launch the app without recompiling or changing any Python file.
3. Open **Edit → Settings...**.
4. **Verify**: "Français" appears in the language dropdown automatically.
