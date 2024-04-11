from typing import Any, Callable, Dict, Iterator, List, Literal, Optional, Set

from typing_extensions import Self

from ..element import Element
from ..events import GenericEventArguments, ValueChangeEventArguments, handle_event
from ..logging import log


class Tree(Element):

    def __init__(self,
                 nodes: List[Dict], *,
                 node_key: str = 'id',
                 label_key: str = 'label',
                 children_key: str = 'children',
                 on_select: Optional[Callable[..., Any]] = None,
                 on_expand: Optional[Callable[..., Any]] = None,
                 on_tick: Optional[Callable[..., Any]] = None,
                 tick_strategy: Optional[Literal['leaf', 'leaf-filtered', 'strict']] = None,
                 ) -> None:
        """Tree

        Display hierarchical data using Quasar's `QTree <https://quasar.dev/vue-components/tree>`_ component.

        If using IDs, make sure they are unique within the whole tree.

        To use checkboxes and ``on_tick``, set the ``tick_strategy`` parameter to "leaf", "leaf-filtered" or "strict".

        :param nodes: hierarchical list of node objects
        :param node_key: property name of each node object that holds its unique id (default: "id")
        :param label_key: property name of each node object that holds its label (default: "label")
        :param children_key: property name of each node object that holds its list of children (default: "children")
        :param on_select: callback which is invoked when the node selection changes
        :param on_expand: callback which is invoked when the node expansion changes
        :param on_tick: callback which is invoked when a node is ticked or unticked
        :param tick_strategy: whether and how to use checkboxes ("leaf", "leaf-filtered" or "strict"; default: ``None``)
        """
        super().__init__('q-tree')
        self._props['nodes'] = nodes
        self._props['node-key'] = node_key
        self._props['label-key'] = label_key
        self._props['children-key'] = children_key
        self._props['selected'] = []
        self._props['expanded'] = []
        self._props['ticked'] = []
        if tick_strategy is not None:
            self._props['tick-strategy'] = tick_strategy
        self._select_handlers = [on_select] if on_select else []
        self._expand_handlers = [on_expand] if on_expand else []
        self._tick_handlers = [on_tick] if on_tick else []

        def update_prop(name: str, value: Any) -> None:
            if self._props[name] != value:
                self._props[name] = value
                self.update()

        def handle_selected(e: GenericEventArguments) -> None:
            update_prop('selected', e.args)
            for handler in self._select_handlers:
                handle_event(handler, ValueChangeEventArguments(sender=self, client=self.client, value=e.args))
        self.on('update:selected', handle_selected)

        def handle_expanded(e: GenericEventArguments) -> None:
            update_prop('expanded', e.args)
            for handler in self._expand_handlers:
                handle_event(handler, ValueChangeEventArguments(sender=self, client=self.client, value=e.args))
        self.on('update:expanded', handle_expanded)

        def handle_ticked(e: GenericEventArguments) -> None:
            update_prop('ticked', e.args)
            for handler in self._tick_handlers:
                handle_event(handler, ValueChangeEventArguments(sender=self, client=self.client, value=e.args))
        self.on('update:ticked', handle_ticked)

    def on_select(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when the selection changes."""
        self._select_handlers.append(callback)
        return self

    def on_expand(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when the expansion changes."""
        self._expand_handlers.append(callback)
        return self

    def on_tick(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when a node is ticked or unticked."""
        self._tick_handlers.append(callback)
        return self

    def expand(self, node_keys: Optional[List[str]] = None) -> Self:
        """Expand the given nodes.

        :param node_keys: list of node keys to expand (default: all nodes)
        """
        self._props['expanded'][:] = self._find_node_keys(node_keys).union(self._props['expanded'])
        self.update()
        return self

    def collapse(self, node_keys: Optional[List[str]] = None) -> Self:
        """Collapse the given nodes.

        :param node_keys: list of node keys to collapse (default: all nodes)
        """
        self._props['expanded'][:] = set(self._props['expanded']).difference(self._find_node_keys(node_keys))
        self.update()
        return self

    def _find_node_keys(self, node_keys: Optional[List[str]] = None) -> Set[str]:
        if node_keys is not None:
            return set(node_keys)

        CHILDREN_KEY = self._props['children-key']
        NODE_KEY = self._props['node-key']

        def iterate_nodes(nodes: List[Dict]) -> Iterator[Dict]:
            for node in nodes:
                yield node
                yield from iterate_nodes(node.get(CHILDREN_KEY, []))
        return {node[NODE_KEY] for node in iterate_nodes(self._props['nodes'])}

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        super().props(add, remove=remove)
        if 'default-expand-all' in self._props:
            # https://github.com/zauberzeug/nicegui/issues/1385
            del self._props['default-expand-all']
            log.warning('The prop "default-expand-all" is not supported by `ui.tree`.\n'
                        'Use ".expand()" instead.')
        return self
