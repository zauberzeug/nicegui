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
                 design: str,
                 value: Any,
                 on_change: Callable):

        super().__init__(view, design)

        self.on_change = on_change
        self.value = value
        self.value.bind_to(self.view.value)

    def handle_change(self, msg):

        self.value = msg['value']

        if self.on_change is not None:
            try:
                try:
                    self.on_change()
                except TypeError:
                    self.on_change(EventArguments(self, value=self.value))
            except Exception:
                traceback.print_exc()

    def bind_value_to(self, target):

        self.value.bind_to(target, nesting=1)
        return self

    def bind_value_from(self, target):

        self.value.bind_from(target, nesting=1)
        return self

    def bind_value(self, target):

        self.value.bind(target, nesting=1)
        return self
