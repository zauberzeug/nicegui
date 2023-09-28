from typing import Any, Callable, List, Literal, Optional

from typing_extensions import Self

from .. import globals  # pylint: disable=redefined-builtin
from ..element import Element
from ..events import GenericEventArguments, ValueChangeEventArguments, handle_event


class Tree(Element):

    def __init__(self, nodes: List, *,
                 node_key: str = 'id',
                 label_key: str = 'label',
                 children_key: str = 'children',
                 on_select: Optional[Callable[..., Any]] = None,
                 on_expand: Optional[Callable[..., Any]] = None,
                 on_tick: Optional[Callable[..., Any]] = None,
                 tick_strategy: Optional[Literal['leaf', 'leaf-filtered', 'strict']] = None,
                 default_expand_all: bool = False,
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
        :param default_expand_all: whether to expand all nodes by default (default: ``False``)
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
        if default_expand_all:
            # https://github.com/zauberzeug/nicegui/issues/1385
            def expand_all(nodes: List) -> None:
                for node in nodes:
                    self._props['expanded'].append(node[node_key])
                    expand_all(node.get(children_key, []))
            expand_all(nodes)

        def update_prop(name: str, value: Any) -> None:
            if self._props[name] != value:
                self._props[name] = value
                self.update()

        def handle_selected(e: GenericEventArguments) -> None:
            update_prop('selected', e.args)
            handle_event(on_select, ValueChangeEventArguments(sender=self, client=self.client, value=e.args))
        self.on('update:selected', handle_selected)

        def handle_expanded(e: GenericEventArguments) -> None:
            update_prop('expanded', e.args)
            handle_event(on_expand, ValueChangeEventArguments(sender=self, client=self.client, value=e.args))
        self.on('update:expanded', handle_expanded)

        def handle_ticked(e: GenericEventArguments) -> None:
            update_prop('ticked', e.args)
            handle_event(on_tick, ValueChangeEventArguments(sender=self, client=self.client, value=e.args))
        self.on('update:ticked', handle_ticked)

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        super().props(add, remove=remove)
        if 'default-expand-all' in self._props:
            del self._props['default-expand-all']
            globals.log.warning('The prop "default_expand_all" is not supported by `ui.tree`.\n'
                                'Use the parameter "default_expand_all" instead.')
        return self
