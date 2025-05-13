from __future__ import annotations

from typing import Any, Dict, List, Optional

from .content import DocumentationPage, registry
from .content.overview import tiles

tree_format_list: List[Dict[str, Any]] = []


def build_tree_format_list() -> None:
    """Build tree format list."""
    tree_format_list.clear()
    for module, _ in tiles:
        page = registry[module.__name__.rsplit('.', 1)[-1]]
        tree_format_list.append({
            'id': page.name,
            'title': _plain(page.title),
            'children': _children(page),
        })


def _children(page: DocumentationPage) -> List[Dict[str, Any]]:
    return [
        {
            'id': part.link if part.link else f'{page.name}#{part.link_target}',
            'title': _plain(part.title),
            'children': _children(registry[part.link]) if part.link else [],
        }
        for part in page.parts
        if part.link or part.link_target
    ]


def _plain(string: Optional[str]) -> str:
    assert string is not None
    return string.replace('*', '')
