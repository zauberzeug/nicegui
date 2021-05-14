import justpy as jp
from typing import Callable
from .string_element import StringElement

class Input(StringElement):

    def __init__(self,
                 *,
                 label: str = None,
                 placeholder: str = None,
                 value: str = '',
                 design: str = '',
                 on_change: Callable = None):

        view = jp.QInput(
            label=label,
            placeholder=placeholder,
            value=value,
            **{key: True for key in design.split()},
            change=self.handle_change,
        )

        super().__init__(view, value=value, on_change=on_change)
