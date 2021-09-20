from typing import Callable
import justpy as jp
from .element import Element
from ..utils import handle_exceptions, provide_arguments


class MenuItem(Element):

    def __init__(self,
                 text: str = '',
                 on_click: Callable = None,
                 ):
        """Menu Item Element

        A menu item to be added to a menu.

        :param text: label of the menu item
        :param on_click: callback to be executed when selecting the menu item
        """
        view = jp.QItem(text=text, clickable=True)

        if on_click is not None:
            view.on('click', handle_exceptions(provide_arguments(on_click)))

        super().__init__(view)
