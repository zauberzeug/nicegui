from typing import Any, Callable, Dict, Optional

import justpy as jp

from ..binding import BindableProperty, bind_from, bind_to
from ..events import ValueChangeEventArguments, handle_event
from .element import Element


class ValueElement(Element):

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

    def bind_value_to(self, target_object, target_name, *, forward=lambda x: x):
        bind_to(self, 'value', target_object, target_name, forward=forward)
        return self

    def bind_value_from(self, target_object, target_name, *, backward=lambda x: x):
        bind_from(self, 'value', target_object, target_name, backward=backward)
        return self

    def bind_value(self, target_object, target_name, *, forward=lambda x: x, backward=lambda x: x):
        bind_from(self, 'value', target_object, target_name, backward=backward)
        bind_to(self, 'value', target_object, target_name, forward=forward)
        return self
