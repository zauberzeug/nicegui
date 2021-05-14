from typing import Callable
import justpy as jp
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Button(Element):

    def __init__(self, text: str, icon: str = None, icon_right: str = None, on_click: Callable = None):

        view = jp.QButton(label=text, color='primary')

        if icon is not None:
            view.icon = icon
        if icon_right is not None:
            view.icon_right = icon_right
        if on_click is not None:
            view.on('click', handle_exceptions(provide_arguments(on_click)))

        super().__init__(view)
