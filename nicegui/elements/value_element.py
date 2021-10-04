import justpy as jp
from typing import Any, Callable
import traceback
from ..binding import bind_from, bind_to, BindableProperty
from ..utils import EventArguments
from .element import Element

class ValueElement(Element):
    value = BindableProperty()

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 *,
                 value: Any,
                 on_change: Callable,
                 ):
        super().__init__(view)

        self.on_change = on_change
        self.value = value
        self.bind_value_to(self.view, 'value', forward=self.value_to_view)

    def value_to_view(self, value):
        return value

    def handle_change(self, msg):
        self.value = msg['value']

        if self.on_change is not None:
            try:
                try:
                    self.on_change()
                except TypeError:
                    self.on_change(EventArguments(self, **msg))
            except Exception:
                traceback.print_exc()

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
