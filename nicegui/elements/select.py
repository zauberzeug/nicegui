import justpy as jp
from typing import Callable, List, Dict, Union
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Select(Element):

    def __init__(self, options: Union[List, Dict], value: any = None, on_change: Callable = None):

        if isinstance(options, list):
            options_ = options
            value_ = value
        else:
            options_ = [{'label': value, 'value': key} for key, value in options.items()]
            value_ = options.get(value)

        view = jp.QSelect(value=value_, options=options_)

        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))

        super().__init__(view)
