"""
Unit tests for i18n components: Translator, LocaleLoader, PreferencesService.
"""
import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch
from src.i18n.translator import Translator
from src.i18n.locale_loader import LocaleLoader
from src.services.preferences_service import PreferencesService


# ---------------------------------------------------------------------------
# Translator Tests
# ---------------------------------------------------------------------------
class TestTranslator:
    def test_translator_returns_active_locale_value(self):
        t = Translator()
        t.load({"btn.save": "Guardar"}, {"btn.save": "Save"})
        assert t.translate("btn.save") == "Guardar"

    def test_translator_falls_back_to_english_for_missing_key(self):
        t = Translator()
        t.load({"btn.cancel": "Cancelar"}, {"btn.save": "Save"})
        assert t.translate("btn.save") == "Save"

    def test_translator_returns_key_when_not_in_any_locale(self):
        t = Translator()
        t.load({}, {})
        assert t.translate("unknown.key") == "unknown.key"

    def test_translator_ignores_empty_string_values(self):
        t = Translator()
        # If a language has a key but empty translation, fallback to English
        t.load({"btn.save": ""}, {"btn.save": "Save"})
        assert t.translate("btn.save") == "Save"


# ---------------------------------------------------------------------------
# LocaleLoader Tests
# ---------------------------------------------------------------------------
class TestLocaleLoader:
    def test_locale_loader_discovers_en(self):
        locales = LocaleLoader.discover()
        assert "en" in locales

    def test_locale_loader_returns_display_name(self):
        locales = LocaleLoader.discover()
        # Depending on if en.json is loaded, it should return English
        if "en" in locales:
            assert locales["en"] == "English"

    def test_load_returns_dict(self):
        data = LocaleLoader.load("en")
        assert isinstance(data, dict)
        if data:
            assert data.get("_meta.language_name") == "English"

    def test_load_unknown_returns_empty(self):
        data = LocaleLoader.load("unknown_lang")
        assert data == {}


# ---------------------------------------------------------------------------
# PreferencesService Tests
# ---------------------------------------------------------------------------
class TestPreferencesService:
    @pytest.fixture(autouse=True)
    def setup_prefs_path(self, tmp_path):
        # Patch the PREFS_PATH to use a temp file for testing
        test_prefs = tmp_path / "test_prefs.json"
        with patch.object(PreferencesService, 'PREFS_PATH', test_prefs):
            yield

    def test_preferences_service_get_default_language(self):
        # Should default to "en" when file doesn't exist
        assert PreferencesService.get_language() == "en"

    def test_preferences_service_round_trip(self):
        PreferencesService.set_language("vi")
        assert PreferencesService.get_language() == "vi"
        
        # Test other generic keys
        PreferencesService.set("theme", "dark")
        assert PreferencesService.get("theme") == "dark"
