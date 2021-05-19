from typing import Callable
import justpy as jp
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Button(Element):

    def __init__(self,
                 text: str = '',
                 *,
                 icon: str = None,
                 icon_right: str = None,
                 color: str = 'primary',
                 text_color: str = None,
                 design: str = '',
                 classes: str = '',
                 on_click: Callable = None):
        """Button Element

        :param text: the label of the button
        :param design: Quasar props to alter the appearance (see `their reference <https://quasar.dev/vue-components/button>`_)
        :param on_click: callback which is invoked when button is pressed
        """

        view = jp.QButton(
            label=text,
            color=color,
            text_color=text_color,
        )

        if icon is not None:
            view.icon = icon

        if icon_right is not None:
            icon_right = icon_right

        if on_click is not None:
            view.on('click', handle_exceptions(provide_arguments(on_click)))

        super().__init__(view, design=design, classes=classes)
