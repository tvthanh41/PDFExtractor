# Phase 0: Research

## Decision 1: Translation Architecture — Custom vs Qt's QTranslator

**Decision**: Use a **custom `Translator` class backed by plain JSON files** rather than Qt's native `.ts`/`.qm` QTranslator mechanism.

**Rationale**:
- Qt's QTranslator requires `lupdate`/`lrelease` toolchain to compile `.ts → .qm` binary files — adds tooling complexity.
- JSON files are human-readable, easily diffable, and can be edited by non-developers or automated via translation APIs.
- A flat `{"key": "value"}` JSON structure is the most portable and simplest format. Used by industry tools like i18next (JS), django-i18n (Python), and Flutter's ARB format.

**Alternatives considered**:
- `gettext / .po files` — well-established but complex toolchain.
- `Qt QTranslator (.ts/.qm)` — requires binary compilation step.
- Python `fluent` library — powerful but heavyweight for this scope.

---

## Decision 2: Key Naming Convention

**Decision**: Flat dot-notation keys: `"<context>.<element>"`.

Examples:
```json
{
  "btn.open_pdf": "Open PDF",
  "btn.add_rule": "Add Rule",
  "tooltip.btn.open_pdf": "Load a PDF file to extract data from.",
  "rule_dialog.label.anchor_text": "Anchor Text:",
  "tooltip.rule_dialog.anchor_text": "The text to search for on the page as a starting reference point.",
  "settings.language": "Language"
}
```

**Rationale**: Flat structure avoids nesting complexity. The `tooltip.` prefix clearly separates label text from tooltip text in the same file.

---

## Decision 3: Translator Singleton / Module-Level Instance

**Decision**: Use a **module-level singleton** — `src/i18n/translator.py` exposes a `translator` instance and a top-level `t(key)` function for convenience.

```python
# src/i18n/translator.py
_instance: Translator = None

def t(key: str) -> str:
    return _instance.translate(key)
```

All UI files import `from src.i18n.translator import t` — clean, no dependency injection needed in widgets.

**Rationale**: Widgets don't need to receive the translator; they just call `t()`. This minimizes changes to existing constructors and keeps the migration incremental.

---

## Decision 4: Language Discovery

**Decision**: Scan `src/i18n/locales/` for `*.json` files at startup. Each file must contain `"_meta.language_name"` key with its display name.

```
locales/
  en.json   → {"_meta.language_name": "English", "btn.open_pdf": "Open PDF", ...}
  vi.json   → {"_meta.language_name": "Tiếng Việt", "btn.open_pdf": "Mở PDF", ...}
```

**Rationale**: Adding a new language = drop a file. No code changes. The `_meta.` prefix makes meta-keys easily distinguishable from UI string keys.

---

## Decision 5: Preferences Storage

**Decision**: Store preferences at `~/.pdftpl_prefs.json` as a simple JSON dict.

```json
{"language": "en"}
```

**Rationale**: Cross-platform home directory via `pathlib.Path.home()`. JSON is readable and editable by power users. No dependency on platform registry or config parsers.

---

## Decision 6: Language Switching Requires Restart

**Decision**: Changing the language in Settings saves the preference and shows a message: *"Please restart the application to apply the new language."*

**Rationale**: Live string switching would require all widgets to subscribe to a language-change signal and re-call `t()` on every string — massive refactoring. Restart-on-change is standard in desktop apps (VS Code, QGIS, etc.) and keeps implementation simple.

---

## Decision 7: Tooltip Strategy — `setToolTip` + `QApplication.setEffectEnabled`

**Decision**: Use Qt's built-in `widget.setToolTip(t("tooltip.xxx"))` on every element. Qt handles display automatically (hover delay, wrapping, styling).

**Rationale**: No third-party library needed. Qt tooltips support rich text (HTML) if needed later.
