import json
from pathlib import Path

from ..examples import examples
from . import registry

PATH = Path(__file__).parent.parent / 'static' / 'search_index.json'


def build_search_index() -> None:
    """Build search index."""
    index = [
        {
            'title': f'{documentation.title.replace("*", "")}: {part.title}',
            'content': part.description,
            'url': f'{documentation.route}#{part.link_target}',
        }
        for documentation in registry.registry.values()
        for part in documentation
    ] + [
        {
            'title': f'Example: {example.title}',
            'content': example.description,
            'url': example.url,
        }
        for example in examples
    ]
    PATH.write_text(json.dumps(index, indent=2))
