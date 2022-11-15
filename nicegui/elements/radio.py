from typing import Any, Callable, Dict, List, Optional, Union

from .choice_element import ChoiceElement


class Radio(ChoiceElement):

    def __init__(self, options: Union[List, Dict], *, value: Any = None, on_change: Optional[Callable] = None):
        """Radio Selection

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        """
        super().__init__(tag='q-option-group', options=options, value=value, on_change=on_change)

    def _msg_to_value(self, msg: Dict) -> Any:
        return self._values[msg['args']]

    def _value_to_model_value(self, value: Any) -> Any:
        return self._values.index(value) if value in self._values else None
