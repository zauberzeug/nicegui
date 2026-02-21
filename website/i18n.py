import csv
import hashlib
import re
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

from nicegui import app

TRANSLATIONS_DIR = Path(__file__).parent / 'translations'

_translations: dict[str, dict[str, str]] = {}
_hashes: dict[str, str] = {}  # english_text -> sha256
_languages: list[str] = ['en']
_language_override: ContextVar[str | None] = ContextVar('_language_override', default=None)


def _sha256(text: str) -> str:
    """Compute the SHA-256 hex digest of a UTF-8 encoded string."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def load() -> None:
    """Load translations from per-language CSV files in the translations directory."""
    global _languages  # noqa: PLW0603
    _translations.clear()
    _hashes.clear()
    if not TRANSLATIONS_DIR.exists():
        return

    en_file = TRANSLATIONS_DIR / 'en.csv'
    if not en_file.exists():
        return

    # Read English strings and build hash -> english mapping
    hash_to_english: dict[str, str] = {}
    with en_file.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            h = row.get('sha256', '')
            text = row.get('text', '')
            if h and text:
                hash_to_english[h] = text
                _hashes[text] = h

    # Discover available languages from CSV files
    _languages = ['en']
    for lang_file in sorted(TRANSLATIONS_DIR.glob('*.csv')):
        lang = lang_file.stem
        if lang != 'en':
            _languages.append(lang)
    # Add sha256 as a virtual language for grep convenience
    if 'sha256' not in _languages:
        _languages.append('sha256')

    # Load each language's translations
    for lang in _languages:
        if lang in ('en', 'sha256'):
            continue
        lang_file = TRANSLATIONS_DIR / f'{lang}.csv'
        if not lang_file.exists():
            continue
        with lang_file.open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                h = row.get('sha256', '')
                text = row.get('text', '')
                if h and text and h in hash_to_english:
                    english = hash_to_english[h]
                    if english not in _translations:
                        _translations[english] = {}
                    _translations[english][lang] = text


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
    if lang == 'sha256':
        return _hashes.get(english, _sha256(english))
    return _translations.get(english, {}).get(lang) or english


_PARAM_RE = re.compile(r'(\s*:param \w+:\s*)(.*)')


def translate_docstring(doc: str) -> str:
    """Translate a docstring, translating intro text and :param descriptions individually."""
    if ':param' not in doc:
        return t(doc)
    lines = doc.splitlines()
    intro_lines: list[str] = []
    param_lines: list[str] = []
    for line in lines:
        if _PARAM_RE.match(line):
            param_lines.append(line)
        else:
            intro_lines.append(line)
    intro = '\n'.join(intro_lines).strip()
    translated_params = []
    for line in param_lines:
        m = _PARAM_RE.match(line)
        if m:
            translated_params.append(f'{m.group(1)}{t(m.group(2))}')
        else:
            translated_params.append(line)
    parts = []
    if intro:
        parts.append(t(intro))
    if translated_params:
        parts.append('\n'.join(translated_params))
    return '\n\n'.join(parts)
