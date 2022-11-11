from typing import Callable, Optional

import justpy as jp

from ..binding import BindableProperty, BindTextMixin
from ..events import ClickEventArguments, handle_event
from .group import Group


class Button(Group, BindTextMixin):
    text = BindableProperty()

    def __init__(self, text: str = '', *, on_click: Optional[Callable] = None):
        """Button

        :param text: the label of the button
        :param on_click: callback which is invoked when button is pressed
        """

        view = jp.QButton(label=text, color='primary', temp=False)
        super().__init__(view)

        self.text = text
        self.bind_text_to(self.view, 'label')

        def process_event(view, event) -> Optional[bool]:
            return handle_event(on_click, ClickEventArguments(sender=self, socket=event.get('websocket')))

        view.on('click', process_event)

    def set_text(self, text: str):
        self.text = text
