from pathlib import Path
from typing import Dict, List

from fastapi.responses import JSONResponse

from nicegui import app

from ..examples import examples
from .content import registry
from .code_extraction import get_full_code

PATH = Path(__file__).parent.parent / 'static' / 'search_index.json'
search_index: List[Dict[str, str]] = []
sitewide_index: List[Dict[str, str]] = []
examples_index: List[Dict[str, str]] = []


@app.get('/static/search_index.json')
def _get_search_index() -> JSONResponse:
    return JSONResponse(search_index)


@app.get('/static/sitewide_index.json')
def _get_sitewide_index() -> JSONResponse:
    return JSONResponse(sitewide_index)


@app.get('/static/examples_index.json')
def _get_examples_index() -> JSONResponse:
    return JSONResponse(examples_index)


def build_search_index() -> None:
    """Build search index."""
    search_index.clear()
    sitewide_index.extend([
        {
            'title': f'{documentation.heading.replace("*", "")}: {part.title}',
            'content': part.description or part.search_text or '',
            'format': part.description_format,
            'demo': get_full_code(part.demo.function) if part.demo is not None else '',
            'url': f'/documentation/{documentation.name}#{part.link_target}',
        }
        for documentation in registry.values()
        for part in documentation.parts
    ])
    search_index.extend([
        {
            'title': f'{documentation.heading.replace("*", "")}: {part.title}',
            'content': part.description or part.search_text or '',
            'format': part.description_format,
            'url': f'/documentation/{documentation.name}#{part.link_target}',
        }
        for documentation in registry.values()
        for part in documentation.parts
    ])
    examples_index.extend([
        {
            'title': f'Example: {example.title}',
            'content': example.description,
            'format': 'md',
            'url': example.url,
        }
        for example in examples
    ])
    search_index.extend(examples_index)
