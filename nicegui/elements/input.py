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
        """Text Input Element.

        Parameters
        ----------
        label : str
            displayed name of the text input


        """
        view = jp.QInput(
            label=label,
            placeholder=placeholder,
            value=value,
            change=self.handle_change,
        )

        super().__init__(view, design, value, on_change)
