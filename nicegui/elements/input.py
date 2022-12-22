from typing import Callable, Optional

from .mixins.value_element import ValueElement


class Input(ValueElement):

    def __init__(self, label: Optional[str] = None, *,
                 placeholder: Optional[str] = None, value: str = '', on_change: Optional[Callable] = None) -> None:
        """Text Input

        :param label: displayed label for the text input
        :param placeholder: text to show if no value is entered
        :param value: the current value of the text input
        :param on_change: callback to execute when the input is confirmed by leaving the focus
        """
        super().__init__(tag='q-input', value=value, on_value_change=on_change)
        self._props['label'] = label
        self._props['placeholder'] = placeholder
