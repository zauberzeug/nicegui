from typing import Callable, Optional

import justpy as jp
from nicegui.events import ValueChangeEventArguments, handle_event

from .element import Element


class Tree(Element):
    def __init__(self, nodes: list, *,
                 node_key: str = 'id',
                 label_key: str = 'label',
                 children_key: str = 'children',
                 on_select: Optional[Callable] = None):
        """Tree

        :param nodes: hierarchical list of node objects
        :param node_key: property name of each node object that holds its unique id (default: "id")
        :param label_key: property name of each node object that holds its label (default: "label")
        :param children_key: property name of each node object that holds its list of children (default: "children")
        :param on_click: callback which is invoked when the node selection changes
        """

        view = jp.QTree(nodes=nodes, node_key=node_key, label_key=label_key, children_key=children_key, temp=False)
        super().__init__(view)

        def process_event(view, event) -> Optional[bool]:
            arguments = ValueChangeEventArguments(sender=self, socket=event.get('websocket'), value=event.get('value'))
            return handle_event(on_select, arguments)

        view.on('update:selected', process_event)
        view.on('update:expanded', lambda *_: self.update())
        view.on('update:ticked', lambda *_: self.update())
