from typing import Any

from ..style import create_anchor_name
from .content import DocumentationPage, registry
from .content.overview import tiles

nodes: list[dict[str, Any]] = []
group_ids: dict[str, str] = {}


def build_tree() -> None:
    """Build tree by recursively collecting documentation pages and parts."""
    nodes.clear()
    group_ids.clear()
    for module, _ in tiles:
        page = registry[module.__name__.rsplit('.', 1)[-1]]
        nodes.append({
            'id': page.name,
            'title': _plain(page.title),
            'children': _children(page),
        })


def _children(page: DocumentationPage) -> list[dict[str, Any]]:
    result = []
    for part in page.parts:
        if part.children:
            group_children = []
            for child in part.children:
                if child.link:
                    group_children.append({
                        'id': child.link,
                        'title': _plain(child.title),
                        'children': _children(registry[child.link]) if child.link in registry else [],
                    })
                elif child.link_target:
                    group_children.append({
                        'id': f'{page.name}#{child.link_target}',
                        'title': _plain(child.title),
                        'children': [],
                    })
            group_id = part.link if part.link else f'{page.name}#{part.link_target}'
            anchor = create_anchor_name(_plain(part.title)) if part.title else ''
            group_ids[group_id] = f'/documentation/{page.name}#{anchor}'
            result.append({
                'id': group_id,
                'title': _plain(part.title),
                'children': group_children,
            })
        elif part.link or part.link_target:
            result.append({
                'id': part.link if part.link else f'{page.name}#{part.link_target}',
                'title': _plain(part.title),
                'children': _children(registry[part.link]) if part.link and part.link in registry else [],
            })
    return result


def _plain(string: str | None) -> str:
    assert string is not None
    return string.replace('*', '')


def ancestors(node_id: str) -> list[str]:
    """Get the ancestors of a node."""
    def _find_path(search_nodes: list[dict[str, Any]], target: str) -> list[str] | None:
        for node in search_nodes:
            if node['id'] == target:
                return [target]
            path = _find_path(node.get('children', []), target)
            if path is not None:
                return [node['id'], *path]
        return None
    return _find_path(nodes, node_id) or [node_id]
