from __future__ import annotations

from typing import Any

from .content import DocumentationPage, registry
from .content.overview import tiles

nodes: list[dict[str, Any]] = []


def build_tree() -> None:
    """Build tree by recursively collecting documentation pages and parts."""
    nodes.clear()
    for module, _ in tiles:
        page = registry[module.__name__.rsplit('.', 1)[-1]]
        nodes.append({
            'id': page.name,
            'title': _plain(page.title),
            'children': _children(page),
        })


def _children(page: DocumentationPage) -> list[dict[str, Any]]:
    return [
        {
            'id': part.link if part.link else f'{page.name}#{part.link_target}',
            'title': _plain(part.title),
            'children': _children(registry[part.link]) if part.link else [],
        }
        for part in page.parts
        if part.link or part.link_target
    ]


def _plain(string: str | None) -> str:
    assert string is not None
    return string.replace('*', '')


def ancestors(node_id: str) -> list[str]:
    """Get the ancestors of a node."""
    parent = next((node for node in nodes if any(child['id'] == node_id for child in node.get('children', []))), None)
    return [node_id] + (ancestors(parent['id']) if parent else [])
