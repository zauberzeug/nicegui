from nicegui.binding import Binding
import justpy as jp
from typing import Callable
from .element import Element
from ..utils import handle_exceptions

class Number(Element):

    def __init__(self,
                 *,
                 label: str = None,
                 placeholder: str = None,
                 value: float = None,
                 decimals: int = None,
                 design: str = '',
                 on_change: Callable = None):

        self.decimals = decimals
        self.on_change = on_change

        view = jp.QInput(
            type='number',
            label=label,
            placeholder=placeholder,
            **{key: True for key in design.split()},
        )
        view.on('change', handle_exceptions(self.handle_change))

        super().__init__(view)

        self.value = value

    @property
    def value(self):

        return self.value_

    @value.setter
    def value(self, value: float):

        self.value_ = value
        if value is None:
            self.view.value = None
        elif self.decimals is None:
            self.view.value = str(value)
        else:
            self.view.value = f'{value:.{self.decimals}f}'

    def handle_change(self, sender, msg):

        self.value = float(msg['value'])

        if self.on_change is not None:
            self.on_change(sender, self.value)

        for binding in self.bindings:
            binding.update_model()
