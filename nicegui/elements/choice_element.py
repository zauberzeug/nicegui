import justpy as jp
from typing import Any, Union, List, Dict, Callable
from .value_element import ValueElement

class ChoiceElement(ValueElement):

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 options: Union[List, Dict],
                 *,
                 value: Any,
                 on_change: Callable):

        if isinstance(options, list):
            view.options = [{'label': option, 'value': option} for option in options]
        else:
            view.options = [{'label': value, 'value': key} for key, value in options.items()]

        super().__init__(view, value=value, on_change=on_change)
