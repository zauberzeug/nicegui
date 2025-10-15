from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from typing import Any, Generic, Optional

from typing_extensions import TypeVar

from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import A, ValueElement

LT = TypeVar('LT', bound=Hashable)
VT = TypeVar('VT', bound=Hashable)
T = TypeVar('T', bound='Option[Any, Any]')


@dataclass
class Option(Generic[LT, VT]):
    label: LT
    value: VT

    def __post_init__(self):
        self.id = f'{hash(self.label)}{hash(self.value)}'


def as_option(val: VT) -> Option[VT, VT]:
    return Option(label=val, value=val)


def _check_values(options: Iterable[T], value: tuple[T, ...]) -> tuple[T, ...]:
    invalid_values: list[Any] = []
    for v in value:
        if v.value not in [o.value for o in options]:
            invalid_values.append(v)
    if invalid_values:
        raise ValueError(f'Invalid values: {",".join(map(lambda o: o.value, invalid_values))}')
    return value


class ChoiceElement(ValueElement[tuple[T, ...], A]):

    def __init__(self, *,
                 tag: Optional[str] = None,
                 options: Iterable[T],
                 value: tuple[T, ...] = (),
                 on_change: Optional[Handler[ValueChangeEventArguments[tuple[T, ...]]]] = None,
                 js_handler: str = ''
                 ) -> None:
        self.options = list(options)
        super().__init__(tag=tag, value=_check_values(options, value), on_value_change=on_change, js_handler=js_handler)
        self._do_updates()
        self._update_options()

    def _do_updates(self) -> None:
        self._values = [o.value for o in self.options]
        self._labels = [o.label for o in self.options]
        self._index_to_option: dict[str, T] = {o.id: o for o in self.options}

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = self.options
        new_val = self._value_to_model_value(before_value)
        self._props[self.VALUE_PROP] = new_val
        self.value = tuple(v for v in before_value if v.id in self._index_to_option)

    def update(self) -> None:
        with self._props.suspend_updates():
            self._do_updates()
            self._update_options()
        super().update()

    def set_options(self, options: Iterable[T], *, value: Optional[tuple[T, ...]] = None) -> None:
        """Set the options of this choice element.

        :param options: The new options.
        :param value: The new value. If not given, the current value is kept.
        """
        self.options = list(options)
        if value is not None:
            self.value = value
        self.update()

    def set_value(self, value: tuple[T, ...]) -> None:
        """Set the value of this element.

        :param value: The value to set.
        """
        self.value = value
