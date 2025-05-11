from typing import Any, List

from .content import registry
from .content.overview import tiles

tree_format_list: List[dict[str, Any]] = []


def build_tree_format_list() -> None:
    """Build tree format list."""
    all_registry_keys = list(registry.keys())

    all_registry_keys.remove('')

    # First build the adjacency list
    adjacency_list: List[tuple[str, str, str]] = []
    for k, _ in tiles:
        adjacency_list.append(('', k.__name__.rpartition(
            '.')[2], registry[k.__name__.rpartition('.')[2]].title))
        all_registry_keys.remove(k.__name__.rpartition('.')[2])

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
                    adjacency_list.append((v, part.link, part.title))
                    all_registry_keys.remove(part.link)
                elif part.link_target:
                    adjacency_list.append((v, f'{v}#{part.link_target}', part.title))
        i += 1

    def add_to_tree(tree, parent_id, child_id, title):
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
    for k, v, t in adjacency_list:
        if k == '':
            tree_format_list.append({'id': v, 'children': [], 'title': t})
        elif not add_to_tree(tree_format_list, k, v, t):
            # Try to add the child to the correct parent in the tree
            # If the parent is not found, create a new top-level node
            tree_format_list.append({'id': k, 'children': [{'id': v, 'children': [], 'title': t}]})
