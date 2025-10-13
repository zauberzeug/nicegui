from pathlib import Path

from fastapi.responses import JSONResponse

from nicegui import app

from ..examples import examples
from .code_extraction import get_full_code
from .content import registry

PATH = Path(__file__).parent.parent / 'static' / 'search_index.json'
search_index: list[dict[str, str]] = []
sitewide_index: list[dict[str, str]] = []
examples_index: list[dict[str, str]] = []


@app.get('/static/search_index.json')
def _get_search_index() -> JSONResponse:
    response = JSONResponse(search_index)
    response.headers['Cache-Control'] = 'public, max-age=86400, immutable'
    return response


@app.get('/static/sitewide_index.json')
def _get_sitewide_index() -> JSONResponse:
    return JSONResponse(sitewide_index)


@app.get('/static/examples_index.json')
def _get_examples_index() -> JSONResponse:
    return JSONResponse(examples_index)


def build_search_index() -> None:
    """Build search index."""
    search_index[:] = _collect_documentation_parts(include_code=False) + _collect_examples()
    sitewide_index[:] = _collect_documentation_parts(include_code=True)
    examples_index[:] = _collect_examples()


def _collect_documentation_parts(*, include_code: bool = False) -> list[dict[str, str]]:
    return [
        {
            'title': f'{documentation.heading.replace("*", "")}: {part.title}',
            'content': part.description or part.search_text or '',
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
            'title': f'Example: {example.title}',
            'content': example.description,
            'format': 'md',
            'url': example.url,
        }
        for example in examples
    ]
