from typing import Any, Callable, Dict, List, Optional, Union

import justpy as jp

from .value_element import ValueElement


class ChoiceElement(ValueElement):

    def __init__(self, view: jp.HTMLBaseComponent, options: Union[List, Dict], *,
                 value: Any, on_change: Optional[Callable] = None) -> None:
        self.options = options
        self._values: List[str] = []
        self._labels: List[str] = []
        self._update_options(view)
        super().__init__(view, value=value, on_change=on_change)

    def value_to_view(self, value: Any):
        try:
            return self._values.index(value)
        except ValueError:
            return value

    def handle_change(self, msg: Dict):
        index = msg['value']['value'] if isinstance(msg['value'], dict) else msg['value']
        msg['index'] = index
        msg['label'] = self._labels[index]
        msg['value'] = self._values[index]
        return super().handle_change(msg)

    def _update_options(self, view: jp.HTMLBaseComponent) -> None:
        self._values = self.options if isinstance(self.options, list) else list(self.options.keys())
        self._labels = self.options if isinstance(self.options, list) else list(self.options.values())
        view.options = [{'value': index, 'label': option} for index, option in enumerate(self._labels)]

    def update(self) -> None:
        self._update_options(self.view)
        super().update()
