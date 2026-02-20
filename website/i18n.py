import csv
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

from nicegui import app

TRANSLATIONS_FILE = Path(__file__).parent / 'translate.csv'

_translations: dict[str, dict[str, str]] = {}
_languages: list[str] = ['en']
_language_override: ContextVar[str | None] = ContextVar('_language_override', default=None)


def load() -> None:
    """Load translations from the CSV file."""
    global _languages  # noqa: PLW0603
    _translations.clear()
    if not TRANSLATIONS_FILE.exists():
        return
    with TRANSLATIONS_FILE.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return
        _languages = list(reader.fieldnames)
        for row in reader:
            english = row.get('en', '').replace('\r\n', '\n')
            if not english:
                continue
            _translations[english] = {
                lang: row.get(lang, '').replace('\r\n', '\n')
                for lang in _languages if lang != 'en'
            }


def get_language() -> str:
    """Get the current language from browser storage."""
    try:
        return app.storage.browser.get('language', 'en')
    except RuntimeError:
        return 'en'


def set_language(lang: str) -> None:
    """Set the current language in browser storage."""
    app.storage.browser['language'] = lang


def languages() -> list[str]:
    """Return the list of available languages."""
    return list(_languages)


@contextmanager
def language(lang: str):
    """Context manager to override the language for all t() calls within the block."""
    token = _language_override.set(lang)
    try:
        yield
    finally:
        _language_override.reset(token)


def t(english: str) -> str:
    """Return the translated string for the current language, falling back to English."""
    override = _language_override.get()
    lang = override if override is not None else get_language()
    if lang == 'en':
        return english
    return _translations.get(english, {}).get(lang) or english
