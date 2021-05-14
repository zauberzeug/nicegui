import justpy as jp
from typing import Any, Callable
import traceback
from .element import Element
from ..utils import EventArguments

class ValueElement(Element):

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 *,
                 value: Any,
                 on_change: Callable):

        super().__init__(view)

        self.on_change = on_change
        self.value = value

    @property
    def value(self):

        return self.value_

    @value.setter
    def value(self, value: any):

        self.value_ = value
        self.set_view_value(value)

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

        for binding in self.bindings:
            if binding.element_attribute == 'value':
                binding.update_model()
