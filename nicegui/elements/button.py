from typing import Callable, Optional

from ..binding import BindTextMixin
from ..element import Element
from ..events import ClickEventArguments, handle_event


class Button(Element, BindTextMixin):

    def __init__(self, text: str = '', *, on_click: Optional[Callable] = None) -> None:
        """Button

        :param text: the label of the button
        :param on_click: callback which is invoked when button is pressed
        """
        super().__init__('q-btn')
        self.text = text
        self.props('color=primary')

        self.on('click', lambda _: handle_event(on_click, ClickEventArguments(sender=self, client=self.client)))
