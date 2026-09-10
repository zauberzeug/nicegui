import dataclasses
from collections.abc import Callable, Mapping
from typing import Any, Generic, TypeVar, cast

from typing_extensions import Self

from ..events import Handler, ValueChangeEventArguments, ValueT
from .mixins.value_element import ValueElement

RESERVED_OPTION_KEYS = ('value', 'label')

OptionT = TypeVar('OptionT')


def _option_fields(option: Any) -> dict[str, Any]:
    """Return the extra client-side properties of a rich option.

    Options which are dataclasses or mappings expose their fields to the client,
    so slots can access them as ``props.opt.<key>``.
    Scalar options (and anything else) contribute nothing.
    """
    if isinstance(option, Mapping):
        fields = dict(option)
    elif dataclasses.is_dataclass(option) and not isinstance(option, type):
        fields = dataclasses.asdict(option)
    else:
        return {}
    return {key: value for key, value in fields.items() if key not in RESERVED_OPTION_KEYS}


class ChoiceElement(ValueElement[ValueT], Generic[OptionT, ValueT]):

    def __init__(self, *,
                 tag: str | None = None,
                 options: list[OptionT] | dict[OptionT, Any],
                 value: ValueT,
                 on_change: Handler[ValueChangeEventArguments[ValueT]] | None = None,
                 option_label: Callable[[OptionT], Any] | None = None,
                 ) -> None:
        self.options: list[OptionT] | dict[OptionT, Any] = options
        self.option_label = option_label
        self._values: list[OptionT] = []
        self._labels: list[Any] = []
        self._update_values_and_labels()
        if not isinstance(value, list) and value is not None and value not in self._values:
            raise ValueError(f'Invalid value: {value}')
        super().__init__(tag=tag, value=value, on_value_change=on_change)
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

    def _update_values_and_labels(self) -> None:
        self._values = self.options if isinstance(self.options, list) else list(self.options.keys())
        if self.option_label is not None:
            self._labels = [self.option_label(value) for value in self._values]
        else:
            self._labels = self.options if isinstance(self.options, list) else list(self.options.values())

    def _option_dict(self, index: int) -> dict[str, Any]:
        """Build the option as sent to the client.

        NOTE: "value" and "label" are written last so a rich option's own fields can never shadow them.
        """
        return {**_option_fields(self._values[index]), 'value': index, 'label': self._labels[index]}

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = [self._option_dict(index) for index in range(len(self._values))]
        self._props[self.VALUE_PROP] = self._value_to_model_value(before_value)
        if not isinstance(before_value, list):  # no need to update value in case of multi-select
            # NOTE: every subclass admits None as a value in the non-multi-select case, but ValueT can't express that
            self.value = before_value if before_value in self._values else cast(ValueT, None)

    def update(self) -> None:
        with self._props.suspend_updates():
            self._update_values_and_labels()
            self._update_options()
        super().update()

    def set_options(self, options: list[OptionT] | dict[OptionT, Any], *, value: Any = ...) -> Self:
        """Set the options of this choice element.

        :param options: The new options.
        :param value: The new value. If not given, the current value is kept.
        """
        self.options = options
        if value is not ...:
            self.value = value
        self.update()
        return self
