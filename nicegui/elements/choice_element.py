from typing import Any, Callable, Dict, List, Optional, Union

import justpy as jp

from .value_element import ValueElement


class ChoiceElement(ValueElement):

    def __init__(self, view: jp.HTMLBaseComponent, options: Union[List, Dict], *,
                 value: Any, on_change: Optional[Callable] = None) -> None:
        self.values = options if isinstance(options, list) else list(options.keys())
        self.labels = options if isinstance(options, list) else list(options.values())
        view.options = [{'value': index, 'label': option} for index, option in enumerate(self.labels)]

        super().__init__(view, value=value, on_change=on_change)

    def value_to_view(self, value: Any):
        try:
            return self.values.index(value)
        except ValueError:
            return value

    def handle_change(self, msg: Dict):
        index = msg['value']['value'] if isinstance(msg['value'], dict) else msg['value']
        msg['index'] = index
        msg['label'] = self.labels[index]
        msg['value'] = self.values[index]
        return super().handle_change(msg)
