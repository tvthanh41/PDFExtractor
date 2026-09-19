# Implementation Plan: UI Localisation & Tooltips (i18n)

**Branch**: `007-featurename-007-i18n-tooltips` | **Date**: 2026-09-19 | **Spec**: specs/007-featurename-007-i18n-tooltips/spec.md

## Summary

Introduces a lightweight i18n layer using flat JSON locale files, a `Translator` singleton, and a `PreferencesService`. All hard-coded UI strings migrate to `t(key)` calls. Every interactive element gets a tooltip sourced from the same catalogue. A new Settings dialog (accessible via Edit menu) allows language selection with restart-to-apply semantics.

## Technical Context

**Language/Version**: Python 3.x

**Primary Dependencies**: PySide6, `pathlib`, `json` (stdlib only — no new third-party deps)

**Storage**: `~/.pdftpl_prefs.json` for user preferences; `src/i18n/locales/*.json` for locale strings

**Testing**: `pytest` (headless unit tests for Translator, LocaleLoader, PreferencesService)

**Target Platform**: Desktop (Windows/macOS/Linux)

**Project Type**: Desktop UI Application

**Performance Goals**: N/A — locale files are tiny, loaded once at startup.

**Constraints**: No new pip dependencies. Language switching requires app restart.

## Constitution Check

- [x] Desktop-First: All changes are PySide6 UI + Python service layer.
- [x] Test-Driven: `Translator` and `LocaleLoader` logic is pure Python, fully unit-testable headlessly.
- [x] Simple and Extensible: Adding a language = one JSON file, no code changes (SC-003).

## Project Structure

### Documentation

```text
specs/007-featurename-007-i18n-tooltips/
├── plan.md
├── research.md
├── data-model.md
└── quickstart.md
```

### Source Code

```text
src/
├── i18n/                               [NEW PACKAGE]
│   ├── __init__.py
│   ├── translator.py                   [NEW] Translator class + t() singleton
│   ├── locale_loader.py                [NEW] Discovers and loads *.json locales
│   └── locales/
│       └── en.json                     [NEW] Full English string catalogue
│
├── services/
│   └── preferences_service.py          [NEW] Read/write ~/.pdftpl_prefs.json
│
├── ui/
│   ├── main_window.py                  [MODIFY] t() strings + Settings menu item
│   ├── workspace_tab.py                [MODIFY] t() strings + tooltips
│   ├── rule_dialog.py                  [MODIFY] t() strings + tooltips
│   ├── batch_config_dialog.py          [MODIFY] t() strings + tooltips
│   └── settings_dialog.py             [NEW] Language selection dialog
│
└── main.py                             [MODIFY] Bootstrap i18n before window creates

tests/
└── unit/
    └── test_i18n.py                    [NEW] Unit tests for Translator + LocaleLoader + PreferencesService
```

**Structure Decision**: Single `src/i18n/` package keeps all translation concerns isolated. The `t()` convenience function is the only import UI files need.

## Proposed Changes

### 1. i18n Package (New)

#### [NEW] `src/i18n/__init__.py`
Empty init to make it a package.

#### [NEW] `src/i18n/translator.py`
- `Translator` class with `load(active, fallback)` and `translate(key)` methods.
- Fallback chain: active locale → English → key itself.
- Module-level `translator` instance and `t(key)` function.

#### [NEW] `src/i18n/locale_loader.py`
- `LocaleLoader.discover()` → `{code: display_name}` dict by scanning `locales/`.
- `LocaleLoader.load(code)` → locale dict, raises `FileNotFoundError` if missing.
- `LocaleLoader.load_english()` → always loads `en.json`.

#### [NEW] `src/i18n/locales/en.json`
Full English catalogue as per `data-model.md` key table.

---

### 2. Services (New)

#### [NEW] `src/services/preferences_service.py`
- `get(key, default)` / `set(key, value)` backed by `~/.pdftpl_prefs.json`.
- `get_language()` → `"en"` default.
- `set_language(code)`.

---

### 3. Main Entry Point (Modify)

#### [MODIFY] `src/main.py`
Bootstrap i18n before any window is created:
```python
from src.i18n import translator, locale_loader
from src.services.preferences_service import PreferencesService

lang = PreferencesService.get_language()
active = locale_loader.LocaleLoader.load(lang)
fallback = locale_loader.LocaleLoader.load_english()
translator.translator.load(active, fallback)
```

---

### 4. UI Updates (Modify)

All UI files replace raw strings with `t(key)` calls and add `widget.setToolTip(t("tooltip.xxx"))`.

#### [MODIFY] `src/ui/main_window.py`
- Menu strings via `t()`.
- Add **Edit** menu with **Settings...** action that opens `SettingsDialog`.

#### [MODIFY] `src/ui/workspace_tab.py`
- All button labels and table headers via `t()`.
- `setToolTip()` on all buttons and table widget.

#### [MODIFY] `src/ui/rule_dialog.py`
- All labels, window titles, button text via `t()`.
- `setToolTip()` on all inputs, combos, spinners.

#### [MODIFY] `src/ui/batch_config_dialog.py`
- All strings via `t()`.
- `setToolTip()` on all path fields.

#### [NEW] `src/ui/settings_dialog.py`
- Language `QComboBox` populated from `LocaleLoader.discover()`.
- On accept: `PreferencesService.set_language(code)` + info message about restart.

---

### 5. Tests (New)

#### [NEW] `tests/unit/test_i18n.py`
- `test_translator_returns_active_locale_value`
- `test_translator_falls_back_to_english_for_missing_key`
- `test_translator_returns_key_when_not_in_any_locale`
- `test_translator_ignores_empty_string_values`
- `test_locale_loader_discovers_en`
- `test_locale_loader_returns_display_name`
- `test_preferences_service_get_default_language`
- `test_preferences_service_round_trip`

## Verification Plan

### Automated Tests
```bash
uv run pytest tests/unit/test_i18n.py -v
uv run pytest tests/ -v
```

### Manual Verification
Follow all 4 scenarios in `quickstart.md`.
