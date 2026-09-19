"""
Translator: lightweight i18n service backed by flat JSON locale files.

Usage:
    from src.i18n.translator import t
    label = t("btn.open_pdf")          # → "Open PDF" (or active locale equivalent)
"""
from __future__ import annotations


class Translator:
    """
    Holds an active locale dict and an English fallback dict.
    Lookup order: active locale → English fallback → key itself.
    """

    def __init__(self) -> None:
        self._active: dict[str, str] = {}
        self._fallback: dict[str, str] = {}

    def load(self, active: dict[str, str], fallback: dict[str, str]) -> None:
        """
        Load the active locale and the English fallback.
        Both should be flat {key: value} dicts as loaded from JSON files.
        """
        self._active = active or {}
        self._fallback = fallback or {}

    def translate(self, key: str) -> str:
        """
        Return the localised string for *key*.

        Fallback chain:
          1. Active locale value (if non-empty string)
          2. English fallback value (if non-empty string)
          3. The key itself (safe, never raises)
        """
        value = self._active.get(key)
        if value:
            return value
        value = self._fallback.get(key)
        if value:
            return value
        return key


# ---------------------------------------------------------------------------
# Module-level singleton — initialised with empty dicts until bootstrap runs
# ---------------------------------------------------------------------------
translator = Translator()


def t(key: str) -> str:
    """Convenience function. Import this in UI modules: ``from src.i18n.translator import t``."""
    return translator.translate(key)
