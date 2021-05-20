import justpy as jp
from typing import Any, Union, List, Dict, Callable
from .value_element import ValueElement

class ChoiceElement(ValueElement):

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 value: Any,
                 options: Union[List, Dict],
                 on_change: Callable,
                 design: str,
                 classes: str,
                 ):

        if isinstance(options, list):
            view.options = [{'label': option, 'value': option} for option in options]
        else:
            view.options = [{'label': value, 'value': key} for key, value in options.items()]

        super().__init__(view, value, on_change, design=design, classes=classes)
