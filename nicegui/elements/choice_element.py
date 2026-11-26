from typing import Any, Self

from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement


class _ChoiceValue(ValueElement._ValueProperty):  # pylint: disable=protected-access

    def __set__(self, owner: Any, value: Any) -> None:
        super().__set__(owner, owner._to_valid_value(value))  # pylint: disable=protected-access


class ChoiceElement(ValueElement[Any]):
    value = _ChoiceValue()

    def __init__(self, *,
                 tag: str | None = None,
                 options: list | dict,
                 value: Any,
                 on_change: Handler[ValueChangeEventArguments[Any]] | None = None,
                 ) -> None:
        self.options = options
        self._values: list[str] = []
        self._labels: list[str] = []
        self._update_values_and_labels()
        if not isinstance(value, list) and value is not None and value not in self._values:
            raise ValueError(f'Invalid value: {value}')
        super().__init__(tag=tag, value=value, on_value_change=on_change)
        with self._props.suspend_updates():
            self._update_options()

    def _render_markdown(self) -> str:
        if self.value is None:
            return ''
        values = self.value if isinstance(self.value, list) else [self.value]
        labels = []
        for value in values:
            try:
                labels.append(str(self._labels[self._values.index(value)]))
            except (ValueError, IndexError):
                labels.append(str(value))
        display = ', '.join(labels)
        form_label = getattr(self, 'label', None) or ''
        return f'{form_label}: {display}' if form_label else display

    def _to_valid_value(self, value: Any) -> Any:
        if isinstance(value, list):
            return value  # a list may hold entries outside the options, as accepted by the constructor
        self._update_values_and_labels()
        return value if value in self._values else None

    def _update_values_and_labels(self) -> None:
        self._values = self.options if isinstance(self.options, list) else list(self.options.keys())
        self._labels = self.options if isinstance(self.options, list) else list(self.options.values())

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = [{'value': index, 'label': option} for index, option in enumerate(self._labels)]
        self._props[self.VALUE_PROP] = self._value_to_model_value(before_value)
        self.value = before_value  # a scalar is re-validated against the current options by _ChoiceValue

    def update(self) -> None:
        with self._props.suspend_updates():
            self._update_values_and_labels()
            self._update_options()
        super().update()

    def set_options(self, options: list | dict, *, value: Any = ...) -> Self:
        """Set the options of this choice element.

        :param options: The new options.
        :param value: The new value. If not given, the current value is kept.
        """
        self.options = options
        if value is not ...:
            self.value = value
        self.update()
        return self
