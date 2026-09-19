"""
Discovers and loads JSON locale files.
"""
import json
from pathlib import Path

class LocaleLoader:
    LOCALES_DIR = Path(__file__).parent / "locales"

    @classmethod
    def discover(cls) -> dict[str, str]:
        """
        Scan LOCALES_DIR for *.json files and return a mapping of
        {language_code: display_name}.
        The language_code is the filename without .json.
        The display_name is read from the `_meta.language_name` key,
        falling back to the language code if missing.
        """
        locales = {}
        if not cls.LOCALES_DIR.exists():
            return locales

        for file_path in cls.LOCALES_DIR.glob("*.json"):
            lang_code = file_path.stem
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                display_name = data.get("_meta.language_name", lang_code)
                locales[lang_code] = display_name
            except Exception:
                # If a file is malformed, we just skip it or fall back to code
                locales[lang_code] = lang_code
        return locales

    @classmethod
    def load(cls, language_code: str) -> dict[str, str]:
        """
        Load the flat JSON dict for the given language code.
        Returns empty dict if the file is missing or invalid.
        """
        file_path = cls.LOCALES_DIR / f"{language_code}.json"
        if not file_path.exists():
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    @classmethod
    def load_english(cls) -> dict[str, str]:
        """
        Always loads en.json as the baseline fallback.
        """
        return cls.load("en")
