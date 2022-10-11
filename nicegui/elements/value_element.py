from typing import Any, Callable, Dict, Optional

import justpy as jp

from ..binding import BindableProperty, BindValueMixin
from ..events import ValueChangeEventArguments, handle_event
from .element import Element


class ValueElement(Element, BindValueMixin):
    value = BindableProperty(on_change=lambda sender, value: handle_event(
        sender.change_handler, ValueChangeEventArguments(sender=sender, socket=None, value=value)))

    def __init__(self, view: jp.HTMLBaseComponent, *, value: Any, on_change: Optional[Callable]) -> None:
        super().__init__(view)

        self.change_handler = on_change
        self.value = value
        self.bind_value_to(self.view, 'value', forward=self.value_to_view)

    def value_to_view(self, value):
        return value

    def set_value(self, value) -> None:
        self.value = value

    def handle_change(self, msg: Dict):
        self.value = msg['value']
        self.update()
        return False
