import justpy as jp
from typing import Any, Callable
import traceback
from binding import BindableProperty
from .element import Element
from ..utils import EventArguments

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
        self.value.bind_to(self.view.value, forward=self.value_to_view)

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

    def bind_value_to(self, target, forward=lambda x: x):

        self.value.bind_to(target, forward=forward, nesting=1)
        return self

    def bind_value_from(self, target, backward=lambda x: x):

        self.value.bind_from(target, backward=backward, nesting=1)
        return self

    def bind_value(self, target, forward=lambda x: x, backward=lambda x: x):

        self.value.bind(target, forward=forward, backward=backward, nesting=1)
        return self
