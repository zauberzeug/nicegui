from typing import Any, Dict, List, Optional, Union

from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement


class ChoiceElement(ValueElement):

    def __init__(self, *,
                 tag: Optional[str] = None,
                 options: Union[List, Dict],
                 value: Any,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        self.options = options
        self._values: List[str] = []
        self._labels: List[str] = []
        self._update_values_and_labels()
        if not isinstance(value, list) and value is not None and value not in self._values:
            raise ValueError(f'Invalid value: {value}')
        super().__init__(tag=tag, value=value, on_value_change=on_change)
        self._update_options()

    def _update_values_and_labels(self) -> None:
        self._values = self.options if isinstance(self.options, list) else list(self.options.keys())
        self._labels = self.options if isinstance(self.options, list) else list(self.options.values())

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = [{'value': index, 'label': option} for index, option in enumerate(self._labels)]
        self._props[self.VALUE_PROP] = self._value_to_model_value(before_value)
        if not isinstance(before_value, list):  # NOTE: no need to update value in case of multi-select
            self.value = before_value if before_value in self._values else None

    def update(self) -> None:
        self._update_values_and_labels()
        self._update_options()
        super().update()

    def set_options(self, options: Union[List, Dict], *, value: Any = ...) -> None:
        """Set the options of this choice element.

        :param options: The new options.
        :param value: The new value. If not given, the current value is kept.
        """
        self.options = options
        if value is not ...:
            self.value = value
        self.update()
