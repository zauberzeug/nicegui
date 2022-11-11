from typing import Callable, Optional

from ..binding import BindTextMixin
from ..element import Element


class Button(Element, BindTextMixin):

    def __init__(self, text: str = '', *, on_click: Optional[Callable] = None) -> None:
        """Button

        :param text: the label of the button
        :param on_click: callback which is invoked when button is pressed
        """
        super().__init__('q-btn')
        self.text = text
        self.props('color=primary')
        self.on('click', on_click)
