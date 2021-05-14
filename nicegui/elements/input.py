import justpy as jp
from typing import Callable
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Input(Element):

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
        )

        if on_change is not None:
            view.on('change', handle_exceptions(provide_arguments(on_change, 'value')))

        super().__init__(view)
