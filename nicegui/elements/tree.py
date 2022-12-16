from typing import Callable, Optional

from nicegui.events import ValueChangeEventArguments, handle_event

from ..element import Element


class Tree(Element):

    def __init__(self, nodes: list, *,
                 node_key: str = 'id',
                 label_key: str = 'label',
                 children_key: str = 'children',
                 on_select: Optional[Callable] = None) -> None:
        """Tree

        Display hierarchical data using Quasar's `QTree <https://quasar.dev/vue-components/tree>`_ component.

        If using IDs, make sure they are unique within the whole tree.

        :param nodes: hierarchical list of node objects
        :param node_key: property name of each node object that holds its unique id (default: "id")
        :param label_key: property name of each node object that holds its label (default: "label")
        :param children_key: property name of each node object that holds its list of children (default: "children")
        :param on_select: callback which is invoked when the node selection changes
        """
        super().__init__('q-tree')
        self._props['nodes'] = nodes
        self._props['node-key'] = node_key
        self._props['label-key'] = label_key
        self._props['children-key'] = children_key
        self._props['selected'] = []

        def handle_selected(msg):
            handle_event(on_select, ValueChangeEventArguments(sender=self, client=self.client, value=msg['args']))
        self.on('update:selected', handle_selected)
