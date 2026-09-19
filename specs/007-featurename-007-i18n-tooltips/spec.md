# Feature Specification: UI Localisation & Tooltips (i18n)

**Feature Branch**: `007-i18n-tooltips`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "We need to add the instruction for each UI element, so that user know that option use for what purpose. Also we need to support translation, for now we only focus on english but later we can add more language. Of course we need a setting so that we can change the language. Please do not hard code anything, we need to design it flexible as possible."

---

## Background

Currently all UI strings (button labels, column headers, dialog titles, error messages, tooltips) are hard-coded English strings scattered throughout `src/ui/`. There is no translation layer, no tooltip system, and no language preference setting.

This feature introduces:
1. A **centralized string catalogue** (`src/i18n/`) that holds all UI strings and tooltips, keyed by ID.
2. A **language loader** that reads locale JSON files at startup and falls back to English.
3. **Tooltips** wired to every meaningful UI element using the same catalogue.
4. A **Language Setting** in a new Settings dialog accessible from the menu.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Centralised String Catalogue & Tooltip Infrastructure (Priority: P1)

All hard-coded strings are moved into locale JSON files under `src/i18n/locales/`. A `Translator` service loads the active locale and exposes a `t(key)` function. All UI files call `t(key)` instead of raw strings. An English locale file (`en.json`) is the baseline.

**Why this priority**: Everything else depends on this infrastructure. Without the catalogue, tooltips and multi-language support have nowhere to pull strings from.

**Independent Test**: Can be tested headlessly — load `en.json`, call `t("btn.open_pdf")`, assert it returns the expected English string. Also verify that requesting an unknown key returns the key itself (safe fallback).

**Acceptance Scenarios**:

1. **Given** the app launches, **When** no language preference is set, **Then** English strings are loaded and all UI labels display correctly.
2. **Given** `en.json` contains a key `"btn.open_pdf": "Open PDF"`, **When** `t("btn.open_pdf")` is called, **Then** `"Open PDF"` is returned.
3. **Given** an unknown key `"unknown.key"` is requested, **When** `t("unknown.key")` is called, **Then** the key itself is returned as a safe fallback (no crash).
4. **Given** a locale file is partially translated, **When** a missing key is requested, **Then** the English fallback value is used.

---

### User Story 2 — Tooltip Display for All UI Elements (Priority: P1)

Every meaningful interactive element has a tooltip whose text is loaded from the locale catalogue. Tooltips describe the purpose of the element in plain language. This applies to: toolbar buttons, rule dialog fields, batch config dialog fields, advanced settings spinners, table columns, and preview labels.

**Why this priority**: This is directly user-facing value — users immediately benefit from guidance without needing documentation.

**Independent Test**: Open any dialog, hover over a field — a tooltip appears within 1 second describing the field's purpose.

**Acceptance Scenarios**:

1. **Given** the main workspace is open, **When** the user hovers over "Open PDF", **Then** a tooltip appears: `"Load a PDF file to extract data from."`.
2. **Given** the Rule Dialog is open, **When** the user hovers over "Anchor Text", **Then** a tooltip appears describing what anchor text does.
3. **Given** the Advanced Settings is expanded in the Rule Dialog, **When** the user hovers over "Offset Distance", **Then** a tooltip explains the pixel distance concept.
4. **Given** any tooltip text, **Then** it is always loaded from the locale catalogue, never hard-coded.

---

### User Story 3 — Language Setting & Runtime Switching (Priority: P2)

A Settings dialog (accessible via the menu) allows the user to select an installed language. The selected language is saved to a preferences file and applied on the next app launch. The UI shows available languages by reading the `src/i18n/locales/` directory at startup.

**Why this priority**: Language selection is only useful once the infrastructure (US1) and strings (US2) are in place.

**Independent Test**: Change language to a second locale (e.g., a partially translated test locale), restart, and verify the translated strings appear.

**Acceptance Scenarios**:

1. **Given** the Settings dialog is open, **When** the user selects a language from a dropdown, **Then** the selection is saved to a preferences file.
2. **Given** a language is saved in preferences, **When** the app starts, **Then** that language's locale file is loaded.
3. **Given** a locale file exists for language X, **When** the app discovers locale files at startup, **Then** language X appears as an option in the Settings language dropdown.
4. **Given** the selected locale file is missing or corrupt, **When** the app starts, **Then** it falls back to English gracefully without crashing.

---

### Edge Cases

- What if the locale JSON is malformed? → Parse error is caught; fall back to English and log a warning.
- What if no locale files are found? → App still launches using hardcoded English as last-resort fallback.
- What if a key has an empty string value in a locale? → Use the English fallback for that key.
- What if the user deletes a locale file between runs? → Fall back to English on next launch.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST centralise all UI strings into locale JSON files under `src/i18n/locales/`.
- **FR-002**: A `Translator` class MUST provide a `t(key: str) -> str` method that returns the localised string or falls back to English, then to the key itself.
- **FR-003**: Available languages MUST be discovered dynamically by reading the `locales/` directory — no hard-coded list of languages.
- **FR-004**: Every interactive UI element MUST have a tooltip loaded from the locale catalogue.
- **FR-005**: A Settings dialog MUST allow the user to select a language from the dynamically discovered list.
- **FR-006**: The selected language MUST be persisted to a preferences file (e.g., `~/.pdftpl_prefs.json`) and loaded on next startup.
- **FR-007**: If the selected locale file is missing or invalid at startup, the system MUST fall back to English without crashing.
- **FR-008**: Each locale JSON file MUST include a `_meta.language_name` key containing the human-readable name of the language (e.g., `"English"`) for display in the Settings dropdown.

### Key Entities

- **`Translator`** (`src/i18n/translator.py`): Singleton-like service holding the active locale dict and fallback English dict. Exposes `t(key)`.
- **`LocaleLoader`** (`src/i18n/locale_loader.py`): Discovers and loads JSON locale files from `src/i18n/locales/`.
- **`PreferencesService`** (`src/services/preferences_service.py`): Reads/writes user preferences (language selection) to a JSON file in the user's home directory.
- **Locale files** (`src/i18n/locales/en.json`, `src/i18n/locales/vi.json`, etc.): Flat JSON dictionaries mapping string keys to translated values. `en.json` is the canonical baseline.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of visible UI strings are sourced from the locale catalogue (no hard-coded display strings remain in `src/ui/`).
- **SC-002**: Every interactive element has a tooltip (verified by a manual review checklist).
- **SC-003**: Adding a new language requires only creating a new `locales/<code>.json` file — no code changes needed.
- **SC-004**: The app never crashes due to a missing or malformed locale file.

## Assumptions

- Locale files use a flat key-value JSON structure (no nesting) for simplicity and easy diff-ability.
- Key naming convention: `"<context>.<element>"` e.g. `"btn.open_pdf"`, `"rule_dialog.anchor_text"`, `"tooltip.offset_distance"`.
- Language switching requires an app restart (live switching is out of scope for v1).
- The preferences file lives at `~/.pdftpl_prefs.json`.
- The initial release ships with only `en.json`; a `vi.json` (Vietnamese) placeholder may be added as a template.
