from typing import Awaitable, Callable, Optional, Union
import justpy as jp

from ..events import ClickEventArguments, handle_event
from .element import Element


class MenuItem(Element):

    def __init__(self,
                 text: str = '',
                 on_click: Optional[Union[Callable, Awaitable]] = None,
                 ):
        """Menu Item Element

        A menu item to be added to a menu.

        :param text: label of the menu item
        :param on_click: callback to be executed when selecting the menu item
        """
        view = jp.QItem(text=text, clickable=True)

        view.on('click', lambda *_: handle_event(on_click, ClickEventArguments(sender=self), update=self.parent_view))

        super().__init__(view)
