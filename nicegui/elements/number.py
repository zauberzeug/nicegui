from typing import Any, Callable, Dict, Optional

from .mixins.value_element import ValueElement


class Number(ValueElement):

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: Optional[float] = None,
                 format: Optional[str] = None,
                 on_change: Optional[Callable] = None) -> None:
        """Number Input

        :param label: displayed name for the number input
        :param placeholder: text to show if no value is entered
        :param value: the initial value of the field
        :param format: a string like '%.2f' to format the displayed value
        :param on_change: callback to execute when the input is confirmed by leaving the focus
        """
        self.format = format
        super().__init__(tag='q-input', value=value, on_value_change=on_change)
        self._props['type'] = 'number'
        self._props['label'] = label
        self._props['placeholder'] = placeholder

    def _msg_to_value(self, msg: Dict) -> Any:
        return float(msg['args'])

    def _value_to_model_value(self, value: Any) -> Any:
        if value is None:
            return None
        elif self.format is None:
            return str(value)
        elif value == '':
            return 0
        else:
            return self.format % float(value)

    def _value_to_event_value(self, value: Any) -> Any:
        return float(value) if value else 0
