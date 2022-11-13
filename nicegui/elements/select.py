from typing import Any, Callable, Dict, List, Optional, Union

from ..events import ValueChangeEventArguments, handle_event
from .choice_element import ChoiceElement


class Select(ChoiceElement):

    def __init__(self, options: Union[List, Dict], *,
                 label: Optional[str] = None, value: Any = None, on_change: Optional[Callable] = None) -> None:
        """Dropdown Selection

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        """
        super().__init__(tag='q-select', options=options, value=value, on_change=on_change)
        self._props['label'] = label

    def _msg_to_value(self, msg: Dict) -> Any:
        return msg['args']['value']

    def _value_to_model(self, value: Any) -> Any:
        return self._labels[self._values.index(value)] if isinstance(value, str) else self._labels[value]

    def _value_to_event_value(self, value: Any) -> Any:
        return self._values[value]
