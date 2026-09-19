"""
Manages user preferences stored in a JSON file in the user's home directory.
"""
import json
from pathlib import Path

class PreferencesService:
    PREFS_PATH = Path.home() / ".pdftpl_prefs.json"

    @classmethod
    def get(cls, key: str, default=None):
        """Get a preference value by key."""
        if not cls.PREFS_PATH.exists():
            return default
        try:
            with open(cls.PREFS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get(key, default)
        except Exception:
            return default

    @classmethod
    def set(cls, key: str, value) -> None:
        """Set a preference value by key and save to disk."""
        data = {}
        if cls.PREFS_PATH.exists():
            try:
                with open(cls.PREFS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        
        data[key] = value
        
        try:
            with open(cls.PREFS_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    @classmethod
    def get_language(cls) -> str:
        """Return the preferred language code, defaulting to 'en'."""
        return cls.get("language", "en")

    @classmethod
    def set_language(cls, code: str) -> None:
        """Set the preferred language code."""
        cls.set("language", code)
