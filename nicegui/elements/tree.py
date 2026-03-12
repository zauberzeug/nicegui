from collections.abc import Iterator
from typing import Any, Literal

from typing_extensions import Self

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..events import GenericEventArguments, Handler, ValueChangeEventArguments, handle_event
from .mixins.filter_element import FilterElement


class Tree(FilterElement):

    @resolve_defaults
    def __init__(self,
                 nodes: list[dict], *,
                 node_key: str = DEFAULT_PROP | 'id',
                 label_key: str = DEFAULT_PROP | 'label',
                 children_key: str = DEFAULT_PROP | 'children',
                 on_select: Handler[ValueChangeEventArguments] | None = None,
                 on_expand: Handler[ValueChangeEventArguments] | None = None,
                 on_tick: Handler[ValueChangeEventArguments] | None = None,
                 tick_strategy: Literal['leaf', 'leaf-filtered', 'strict'] | None = DEFAULT_PROP | None,
                 ) -> None:
        """Tree

        Display hierarchical data using Quasar's `QTree <https://quasar.dev/vue-components/tree>`_ component.
        Updates can be pushed to the tree by updating ``.props['nodes']``.

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
        super().__init__(tag='q-tree', filter=None)
        self._props['nodes'] = nodes
        self._props['node-key'] = node_key
        self._props['label-key'] = label_key
        self._props['children-key'] = children_key
        if on_select:
            self._props['selected'] = None
        if on_expand:
            self._props['expanded'] = []
        if on_tick or tick_strategy:
            self._props['ticked'] = []
            self._props['tick-strategy'] = tick_strategy or 'leaf'
        self._select_handlers = [on_select] if on_select else []
        self._expand_handlers = [on_expand] if on_expand else []
        self._tick_handlers = [on_tick] if on_tick else []

        # https://github.com/zauberzeug/nicegui/issues/1385
        self._props.add_warning('default-expand-all',
                                'The prop "default-expand-all" is not supported by `ui.tree`. '
                                'Use ".expand()" instead.')

        def update_prop(name: str, value: Any) -> None:
            if self._props[name] != value:
                self._props[name] = value

        def handle_selected(e: GenericEventArguments) -> None:
            previous_value = self._props.get('selected')
            update_prop('selected', e.args)
            args = ValueChangeEventArguments(sender=self, client=self.client,
                                             value=e.args, previous_value=previous_value)
            for handler in self._select_handlers:
                handle_event(handler, args)
        self.on('update:selected', handle_selected)

        def handle_expanded(e: GenericEventArguments) -> None:
            previous_value = self._props.get('expanded')
            update_prop('expanded', e.args)
            args = ValueChangeEventArguments(sender=self, client=self.client,
                                             value=e.args, previous_value=previous_value)
            for handler in self._expand_handlers:
                handle_event(handler, args)
        self.on('update:expanded', handle_expanded)

        def handle_ticked(e: GenericEventArguments) -> None:
            previous_value = self._props.get('ticked')
            update_prop('ticked', e.args)
            args = ValueChangeEventArguments(sender=self, client=self.client,
                                             value=e.args, previous_value=previous_value)
            for handler in self._tick_handlers:
                handle_event(handler, args)
        self.on('update:ticked', handle_ticked)

    def on_select(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """Add a callback to be invoked when the selection changes."""
        self._props.setdefault('selected', None)
        self._select_handlers.append(callback)
        return self

    def select(self, node_key: str | None) -> Self:
        """Select the given node.

        :param node_key: node key to select
        """
        self._props.setdefault('selected', None)
        if self._props['selected'] != node_key:
            self._props['selected'] = node_key
        return self

    def deselect(self) -> Self:
        """Remove node selection."""
        return self.select(None)

    def on_expand(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """Add a callback to be invoked when the expansion changes."""
        self._props.setdefault('expanded', [])
        self._expand_handlers.append(callback)
        return self

    def on_tick(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """Add a callback to be invoked when a node is ticked or unticked."""
        self._props.setdefault('ticked', [])
        self._props.setdefault('tick-strategy', 'leaf')
        self._tick_handlers.append(callback)
        return self

    def tick(self, node_keys: list[str] | None = None) -> Self:
        """Tick the given nodes.

        :param node_keys: list of node keys to tick or ``None`` to tick all nodes (default: ``None``)
        """
        self._props.setdefault('ticked', [])
        self._props['ticked'][:] = self._find_node_keys(node_keys).union(self._props['ticked'])
        return self

    def untick(self, node_keys: list[str] | None = None) -> Self:
        """Remove tick from the given nodes.

        :param node_keys: list of node keys to untick or ``None`` to untick all nodes (default: ``None``)
        """
        self._props.setdefault('ticked', [])
        self._props['ticked'][:] = set(self._props['ticked']).difference(self._find_node_keys(node_keys))
        return self

    def expand(self, node_keys: list[str] | None = None) -> Self:
        """Expand the given nodes.

        :param node_keys: list of node keys to expand (default: all nodes)
        """
        self._props.setdefault('expanded', [])
        self._props['expanded'][:] = self._find_node_keys(node_keys).union(self._props['expanded'])
        return self

    def collapse(self, node_keys: list[str] | None = None) -> Self:
        """Collapse the given nodes.

        :param node_keys: list of node keys to collapse (default: all nodes)
        """
        self._props.setdefault('expanded', [])
        self._props['expanded'][:] = set(self._props['expanded']).difference(self._find_node_keys(node_keys))
        return self

    def nodes(self, *, visible: bool | None = None) -> Iterator[dict]:
        """Iterate over all nodes.

        :param visible: if ``True``, only visible nodes are returned; if ``False``, only invisible nodes are returned; if ``None``, all nodes are returned (default: ``None``)
        """
        def iterate_nodes(nodes: list[dict]) -> Iterator[dict]:
            expanded = self._props.get('expanded')
            NODE_KEY = self._props['node-key']
            CHILDREN_KEY = self._props['children-key']
            for node in nodes:
                yield node
                is_expanded = expanded is None or node[NODE_KEY] in expanded
                if (is_expanded and visible is not False) or (not is_expanded and visible is not True):
                    yield from iterate_nodes(node.get(CHILDREN_KEY, []))
        return iterate_nodes(self._props['nodes'])

    def _find_node_keys(self, node_keys: list[str] | None = None) -> set[str]:
        if node_keys is not None:
            return set(node_keys)
        return {node[self._props['node-key']] for node in self.nodes()}
