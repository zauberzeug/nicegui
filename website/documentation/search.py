from pathlib import Path

from fastapi import Query
from fastapi.responses import JSONResponse

from nicegui import app

from ..examples import examples
from ..i18n import language, t, translate_docstring
from .code_extraction import get_full_code
from .content import registry

PATH = Path(__file__).parent.parent / 'static' / 'search_index.json'
search_index: dict[str, list[dict[str, str]]] = {}
sitewide_index: dict[str, list[dict[str, str]]] = {}
examples_index: dict[str, list[dict[str, str]]] = {}


@app.get('/static/search_index.json')
def _get_search_index(lang: str = Query('en')) -> JSONResponse:
    response = JSONResponse(_get_entries(search_index, lang, _build_search))
    response.headers['Cache-Control'] = 'public, max-age=86400, immutable'
    return response


@app.get('/static/sitewide_index.json')
def _get_sitewide_index(lang: str = Query('en')) -> JSONResponse:
    return JSONResponse(_get_entries(sitewide_index, lang, _build_sitewide))


@app.get('/static/examples_index.json')
def _get_examples_index(lang: str = Query('en')) -> JSONResponse:
    return JSONResponse(_get_entries(examples_index, lang, _build_examples))


def build_search_index() -> None:
    """Build search index."""
    search_index.clear()
    sitewide_index.clear()
    examples_index.clear()
    search_index['en'] = _build_search()
    sitewide_index['en'] = _build_sitewide()
    examples_index['en'] = _build_examples()


def _get_entries(index, lang, build):
    """Return entries for the given language, building and caching lazily."""
    if lang not in index:
        with language(lang):
            index[lang] = build()
    return index[lang]


def _build_search():
    return _collect_documentation_parts(include_code=False) + _collect_examples()


def _build_sitewide():
    return _collect_documentation_parts(include_code=True)


def _build_examples():
    return _collect_examples()


def _collect_documentation_parts(*, include_code: bool = False) -> list[dict[str, str]]:
    return [
        {
            'title': f'{t(documentation.heading.replace("*", ""))}: {t(part.title or "")}',
            'content': translate_docstring(part.description or part.search_text or ''),
            'format': part.description_format,
            **({'demo': get_full_code(part.demo.function) if part.demo is not None else ''} if include_code else {}),
            'url': f'/documentation/{documentation.name}#{part.link_target}',
        }
        for documentation in registry.values()
        for part in documentation.parts
    ]


def _collect_examples() -> list[dict[str, str]]:
    return [
        {
            'title': f'{t("Example")}: {t(example.title)}',
            'content': t(example.description),
            'format': 'md',
            'url': example.url,
        }
        for example in examples
    ]
