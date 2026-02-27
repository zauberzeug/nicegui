"""Internationalization (i18n) support for the NiceGUI website.

Provides a simple translation function ``t()`` backed by per-language JSON files.
Language is resolved per-request via a ``ContextVar``, which is async-safe.
"""
from __future__ import annotations

import json
from contextvars import ContextVar
from pathlib import Path

# URL slug -> display name
SUPPORTED_LANGUAGES: dict[str, str] = {
    'en': 'English',
    'de': 'Deutsch',
    'ja': '日本語',
    'ko': '한국어',
    'zh': '中文',
}

_TRANSLATIONS_DIR = Path(__file__).parent / 'translations'

_current_language: ContextVar[str] = ContextVar('_current_language', default='en')
_url_prefix: ContextVar[str] = ContextVar('_url_prefix', default='')

_cache: dict[str, dict[str, str]] = {}


def _load_translations(lang: str) -> dict[str, str]:
    """Load translation dict for *lang*, returning cached copy if available."""
    if lang not in _cache:
        path = _TRANSLATIONS_DIR / f'{lang}.json'
        if path.exists():
            _cache[lang] = json.loads(path.read_text(encoding='utf-8'))
        else:
            _cache[lang] = {}
    return _cache[lang]


def set_language(lang: str) -> None:
    """Set the language for the current request context."""
    _current_language.set(lang)
    _url_prefix.set(f'/{lang}' if lang != 'en' else '')


def get_language() -> str:
    """Return the current request language."""
    return _current_language.get()


def get_url_prefix() -> str:
    """Return the URL path prefix for the current language (empty for English)."""
    return _url_prefix.get()


def t(english: str) -> str:
    """Look up a translated string for the current language.

    Uses the English text as the lookup key.  Falls back to the original
    English string when no translation is available.  Internal documentation
    links are rewritten to include the current language prefix.
    """
    lang = _current_language.get()
    if lang == 'en':
        return english
    text = _load_translations(lang).get(english, english)
    prefix = _url_prefix.get()
    if prefix and '](' in text:
        text = text.replace('](/', f']({prefix}/')
    return text
