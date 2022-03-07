from typing import Awaitable, Callable, Optional, Union
import justpy as jp

from ..events import ClickEventArguments, handle_event
from .element import Element


class MenuItem(Element):

    def __init__(self,
                 text: str = '',
                 on_click: Optional[Union[Callable, Awaitable]] = None,
                 *,
                 auto_close: bool = True,
                 ):
        """Menu Item Element

        A menu item to be added to a menu.

        :param text: label of the menu item
        :param on_click: callback to be executed when selecting the menu item
        :param auto_close: whether the menu should be closed after a click event (default: `True`)
        """
        view = jp.QItem(text=text, clickable=True, temp=False)

        def handle_click(*_):
            handle_event(on_click, ClickEventArguments(sender=self), update=self.parent_view)
            if auto_close:
                assert isinstance(self.parent_view, jp.QMenu)
                self.parent_view.value = False

        view.on('click', handle_click)

        super().__init__(view)
