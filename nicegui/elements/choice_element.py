from dataclasses import dataclass
from typing import Any, Collection, Generic, Optional

from typing_extensions import TypeVar

from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement

LT = TypeVar("LT")
VT = TypeVar("VT")
T = TypeVar("T", bound="Option[Any, Any]")
V = TypeVar("V")


@dataclass
class Option(Generic[LT, VT]):
    label: LT
    value: VT


def as_option(val: V) -> Option[V, V]:
    return Option(label=val, value=val)


class ChoiceElement(ValueElement[tuple[T, ...]]):

    def __init__(self, *,
                 tag: Optional[str] = None,
                 options: Collection[T],
                 value: tuple[T, ...] = (),
                 on_change: Optional[Handler[ValueChangeEventArguments[tuple[T, ...]]]] = None,
                 ) -> None:
        self.options = list(options)
        self._update_values_and_labels()
        if (invalid_values := set(o.value for o in value) - set(o.value for o in options)):
            raise ValueError(f'Invalid values: {",".join(map(lambda o: o.value, invalid_values))}')
        super().__init__(tag=tag, value=value, on_value_change=on_change)
        self._update_options()

    def _update_values_and_labels(self) -> None:
        self._values = [o.value for o in self.options]
        self._labels = [o.label for o in self.options]

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = self.options
        self._props[self.VALUE_PROP] = self._value_to_model_value(before_value)

    def update(self) -> None:
        with self._props.suspend_updates():
            self._update_values_and_labels()
            self._update_options()
        super().update()

    def set_options(self, options: list[T], *, value: Optional[tuple[T, ...]] = None) -> None:
        """Set the options of this choice element.

        :param options: The new options.
        :param value: The new value. If not given, the current value is kept.
        """
        self.options = options
        if value is not None:
            self.value = value
        self.update()

    def set_value(self, value: tuple[T, ...]) -> None:
        """Set the value of this element.

        :param value: The value to set.
        """
        self.value = value

