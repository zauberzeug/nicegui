from pathlib import Path
from typing import Dict, List

from fastapi.responses import JSONResponse

from nicegui import app

from ..examples import examples
from .content import registry

PATH = Path(__file__).parent.parent / 'static' / 'search_index.json'
search_index: List[Dict[str, str]] = []


@app.get('/static/search_index.json')
def _get_search_index() -> JSONResponse:
    return JSONResponse(search_index)


def build_search_index() -> None:
    """Build search index."""
    search_index.clear()
    search_index.extend([
        {
            'title': f'{documentation.heading.replace("*", "")}: {part.title}',
            'content': part.description or '',
            'url': f'/documentation/{documentation.name}#{part.link_target}',
        }
        for documentation in registry.values()
        for part in documentation.parts
    ])
    search_index.extend([
        {
            'title': f'Example: {example.title}',
            'content': example.description,
            'url': example.url,
        }
        for example in examples
    ])
