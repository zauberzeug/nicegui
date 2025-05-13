from typing import Any, Dict, List, Tuple

from .content import registry
from .content.overview import tiles

Node = Dict[str, Any]

tree_format_list: List[Node] = []


def build_tree_format_list() -> None:
    """Build tree format list."""
    # First build the adjacency list
    adjacency_list: List[Tuple[str, str, str]] = []
    for module, _ in tiles:
        name = module.__name__.rsplit('.', 1)[-1]
        adjacency_list.append(('', name, registry[name].title or ''))

    i = 0
    while i < len(adjacency_list):
        if i > 1000000:
            break  # no way
        _, v, _ = adjacency_list[i]
        if '#' in v:
            i += 1
            continue
        registry_entry = registry.get(v)
        if registry_entry and registry_entry.parts:
            for part in registry_entry.parts:
                if part.link:
                    adjacency_list.append((v, part.link, part.title or ''))
                elif part.link_target:
                    adjacency_list.append((v, f'{v}#{part.link_target}', part.title or ''))
        i += 1

    def add_to_tree(tree: List[Node], parent_id: str, child_id: str, title: str) -> bool:
        for node in tree:
            if node['id'] == parent_id:
                node['children'].append({'id': child_id, 'children': [], 'title': title})
                return True
            # Recursively search in the children
            if add_to_tree(node['children'], parent_id, child_id, title):
                return True
        return False

    adjacency_list = [(k, v, t.replace('*', '')) for k, v, t in adjacency_list]

    # Build the tree from adjacency list
    tree_format_list.clear()
    for key, v, title in adjacency_list:
        if key == '':
            tree_format_list.append({'id': v, 'children': [], 'title': title})
        elif not add_to_tree(tree_format_list, key, v, title):
            # Try to add the child to the correct parent in the tree
            # If the parent is not found, create a new top-level node
            tree_format_list.append({'id': key, 'children': [{'id': v, 'children': [], 'title': title}]})
