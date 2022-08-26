from typing import Callable, Optional

import justpy as jp

from ..binding import BindableProperty, bind_from, bind_to
from ..events import ClickEventArguments, handle_event
from .element import Element


class Button(Element):
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

    def bind_text_to(self, target_object, target_name, forward=lambda x: x):
        bind_to(self, 'text', target_object, target_name, forward=forward)
        return self

    def bind_text_from(self, target_object, target_name, backward=lambda x: x):
        bind_from(self, 'text', target_object, target_name, backward=backward)
        return self

    def bind_text(self, target_object, target_name, forward=lambda x: x, backward=lambda x: x):
        bind_from(self, 'text', target_object, target_name, backward=backward)
        bind_to(self, 'text', target_object, target_name, forward=forward)
        return self
