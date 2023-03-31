import re
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Union

from nicegui.dependencies import register_component

from .choice_element import ChoiceElement

register_component('select', __file__, 'select.js')


class Select(ChoiceElement):

    def __init__(self, options: Union[List, Dict], *,
                 label: Optional[str] = None,
                 value: Any = None,
                 on_change: Optional[Callable] = None,
                 with_input: bool = False) -> None:
        """Dropdown Selection

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param with_input: whether to show an input field to filter the options
        """
        super().__init__(tag='select', options=options, value=value, on_change=on_change)
        self._props['label'] = label
        if with_input:
            self.original_options = deepcopy(options)
            self._props['use-input'] = True
            self._props['hide-selected'] = True
            self._props['fill-input'] = True
            self._props['input-debounce'] = 0

    def on_filter(self, event: Dict) -> None:
        self.options = [
            option
            for option in self.original_options
            if not event['args'] or re.search(event['args'], option, re.IGNORECASE)
        ]
        self.update()

    def _msg_to_value(self, msg: Dict) -> Any:
        return self._values[msg['args']['value']]

    def _value_to_model_value(self, value: Any) -> Any:
        try:
            index = self._values.index(value)
            return {'value': index, 'label': self._labels[index]}
        except ValueError:
            return None
