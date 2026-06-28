from copy import deepcopy
from typing import Any

from typing_extensions import Self

from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement

# Scalar types whose values are never mutated in place; the shallow-copied snapshot can be
# compared by value without needing deepcopy.
_IMMUTABLE_OPTION_TYPES = frozenset({str, int, float, bool, type(None)})


class ChoiceElement(ValueElement[Any]):

    def __init__(self, *,
                 tag: str | None = None,
                 options: list | dict,
                 value: Any,
                 on_change: Handler[ValueChangeEventArguments[Any]] | None = None,
                 ) -> None:
        self.options = options
        self._values: list[Any] = []
        self._labels: list[Any] = []
        self._update_values_and_labels()
        self._options_snapshot = self._create_options_snapshot()
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

    def _update_values_and_labels(self) -> None:
        if isinstance(self.options, list):
            self._values = self.options
            self._labels = self.options
        else:
            self._values = list(self.options)
            self._labels = list(self.options.values())

    def _options_have_changed(self) -> bool:
        """Return whether options need to be rebuilt for the client."""
        values_snapshot, labels_snapshot = self._options_snapshot
        if isinstance(self.options, list):
            return self.options != values_snapshot
        return list(self.options) != values_snapshot or list(self.options.values()) != labels_snapshot

    def _create_options_snapshot(self) -> tuple[list[Any], list[Any]]:
        """Capture the option state represented in client props.

        List options are both values and labels. Dict labels are client-visible and may be mutable; dict keys are copied
        shallowly because mutating keys in place would violate Python's hash contract.
        """
        if isinstance(self.options, list):
            values_snapshot = self._copy_options_for_snapshot(self._values)
            return values_snapshot, values_snapshot
        return list(self._values), self._copy_options_for_snapshot(self._labels)

    @staticmethod
    def _copy_options_for_snapshot(options: list[Any]) -> list[Any]:
        """Deep-copy options when possible without rejecting valid non-copyable values."""
        options_snapshot = list(options)
        for option in options_snapshot:
            if type(option) not in _IMMUTABLE_OPTION_TYPES:
                break
        else:  # all options are immutable -> the shallow copy is a valid snapshot
            return options_snapshot
        try:
            return deepcopy(options_snapshot)
        except Exception:  # some valid option objects are not deepcopy-able
            return options_snapshot

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = [{'value': index, 'label': option} for index, option in enumerate(self._labels)]
        self._props[self.VALUE_PROP] = self._value_to_model_value(before_value)
        self._options_snapshot = self._create_options_snapshot()
        if not isinstance(before_value, list):  # no need to update value in case of multi-select
            self.value = before_value if before_value in self._values else None

    def update(self) -> None:
        if self._options_have_changed():
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
