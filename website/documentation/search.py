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
    """
    Retrieves the search index.

    This function returns the search index used for searching the documentation.
    The search index is a JSON object containing information about the available
    documentation pages and their corresponding metadata.

    Returns:
        JSONResponse: The search index as a JSON response.

    Example:
        >>> search_index = _get_search_index()
    """
    return JSONResponse(search_index)


def build_search_index() -> None:
    """
    Build search index.

    This function builds the search index used for searching documentation and examples.
    It populates the `search_index` list with dictionaries containing information about
    documentation parts and examples.

    The search index is built by iterating over all the documentation objects in the
    `registry` and their corresponding parts. For each part, a dictionary is created
    with the title, content, and URL. The title is constructed by combining the heading
    of the documentation and the title of the part. The content is the description of
    the part, if available. The URL is generated based on the documentation name and
    the link target of the part.

    After populating the search index with documentation parts, it is extended with
    dictionaries representing examples. Each example dictionary contains the title,
    description, and URL of the example.

    Note: The `search_index` list is assumed to be a global variable.

    Usage:
    - Call this function to build the search index before performing any search operations.
    - The search index can be accessed and used for searching documentation and examples.

    Example:
    >>> build_search_index()
    >>> search('button')  # Search for documentation parts and examples related to 'button'
    """
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
