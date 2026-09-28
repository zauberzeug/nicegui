import functools
import json
from pathlib import Path
from typing import NamedTuple

from nicegui import app
from nicegui.helpers import remove_indentation
from nicegui.language import Language as LanguageCode

TRANSLATIONS_PATH = Path(__file__).parent / 'translations'


class Language(NamedTuple):
    name: str
    '''native display name, e.g. for the language switcher'''
    code: LanguageCode
    '''language code for hreflang links, the ``lang`` attribute of the ``html`` tag and Quasar's language pack'''


LANGUAGES = {
    'en': Language('English', 'en-US'),
    'zh': Language('中文', 'zh-CN'),
}


def set_language(language: str) -> None:
    """Set the language for the current client."""
    app.storage.client['language'] = language


def get_language() -> str:
    """Return the language of the current client (``"en"`` outside of a client context)."""
    try:
        return app.storage.client.get('language', 'en')
    except RuntimeError:
        return 'en'


PAGE_PATHS = ('/documentation', '/examples', '/imprint_privacy')


def url(path: str, *, language: str | None = None) -> str:
    """Prefix an internal *path* with the URL prefix of the given or current language."""
    language = language or get_language()
    if language == 'en' or not path.startswith('/'):
        return path
    if path == '/':
        return f'/{language}'
    if path.startswith('/#'):
        return f'/{language}{path.removeprefix("/")}'
    return f'/{language}{path}'


def alternates(path: str) -> list[tuple[str, str]]:
    """Return the ``hreflang`` alternates of an unprefixed *path* as (language code, prefixed path) pairs.

    The list ends with the ``x-default`` entry pointing to the English page.
    """
    links = [(language.code, url(path, language=slug)) for slug, language in LANGUAGES.items()]
    return [*links, ('x-default', path)]


def t(english: str) -> str:
    """Return the translation of the dedented *english* text for the current client's language.

    The dedented English text serves as the lookup key.
    Untranslated texts fall back to English.
    Links to sub pages in the (translated) Markdown are rewritten to keep the language prefix.
    """
    english = remove_indentation(english)
    language = get_language()
    if language == 'en':
        return english
    text = _translations(language).get(english, english)
    for path in PAGE_PATHS:
        text = text.replace(f']({path}', f'](/{language}{path}')
    return text.replace('](/#', f'](/{language}#')


@functools.cache
def _translations(language: str) -> dict[str, str]:
    path = TRANSLATIONS_PATH / f'{language}.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
