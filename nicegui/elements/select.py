import justpy as jp
from typing import Callable, List
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Select(Element):

    def __init__(self, options: List[str], value: str = None, on_change: Callable = None):

        view = jp.QSelect(value=value, options=options)

        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))

        super().__init__(view)
