from typing import Any, cast, Optional, Union, Generic, Iterable, overload
from typing_extensions import TypeVar, TypedDict


from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement
from dataclasses import dataclass
import hashlib

JsonPrimitive = Union[str, int, float, bool]
JsonValue = Union[
    JsonPrimitive, list[str], list[int], list[float], list[bool], 'list[JsonValue]', 
    dict[str, str], dict[str, int], dict[str, float], dict[str, bool], 'dict[str, JsonValue]'
]

L = TypeVar('L', bound=JsonPrimitive)
V = TypeVar('V', bound=JsonValue)
T = TypeVar('T', bound='Option[Any, Any]')
P = TypeVar('P', str, int, float, bool)
VAL = TypeVar('VAL', bound='Union[tuple[Option[Any, Any], ...], tuple[JsonPrimitive, ...], Optional[JsonPrimitive], Optional[Option[Any, Any]]]')
class DEFAULT: pass


@dataclass
class Option(Generic[L, V]):
    label: L
    value: V

    def __post_init__(self) -> None:
        self.id = hashlib.md5(f"{self.label}{self.value}".encode()).hexdigest()


class OptionDict(TypedDict, Generic[L, V]):
    label: L
    value: V
    id: str


def dict_to_option(v: OptionDict[L, V]) -> Option[L, V]:
    option = Option[L, V](label=v['label'], value=v['value'])
    assert option.id == v['id']
    return option


@overload
def to_option(v: L) -> Option[L, L]:
    ...

@overload
def to_option(v: Option[L, V]) -> Option[L, V]:
    ...


def to_option(v: Union[L, Option[L, V]]) -> Union[Option[L, V], Option[L, L]]:
    if isinstance(v, Option):
        return v
    return Option(label=v, value=v)


class ChoiceElement(ValueElement[VAL], Generic[VAL, T]):

    def __init__(self, *,
                 tag: Optional[str] = None,
                 options: Iterable[T],
                 value: VAL = None,
                 on_change: Optional[Handler[ValueChangeEventArguments[VAL]]] = None,
                 ) -> None:
        self.value = value
        self.options = list(options)
        self._values = [o.value for o in self.options]
        self._labels = [o.label for o in self.options]
        self._id_to_option = {o.id: o for o in self.options}
        if isinstance(self.value, tuple):
            if (invalid_values := set(to_option(v).value for v in self.value) - set(o.value for o in self.options)):
                raise ValueError(f'Invalid values: {invalid_values}')
        elif self.value and to_option(self.value).value not in [o.value for o in self.options]:
            raise ValueError(f'Invalid value: {value}')
        super().__init__(tag=tag, value=value, on_value_change=on_change)
        self._update_options()

    def _update_values_and_labels(self) -> None:
        self._values = [o.value for o in self.options]
        self._labels = [o.label for o in self.options]
        self._id_to_option = {o.id: o for o in self.options}

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = self.options
        new_value = self._value_to_model_value(before_value)
        self._props[self.VALUE_PROP] = new_value
        self.value = new_value

    def update(self) -> None:
        with self._props.suspend_updates():
            self._update_values_and_labels()
            self._update_options()
        super().update()

    def set_options(self, options: Iterable[T], *, value: Union[VAL, DEFAULT] = DEFAULT()) -> None:
        """Set the options of this choice element.

        :param options: The new options.
        :param value: The new value. If not given, the current value is kept.
        """
        self.options = list(options)
        if not isinstance(value, DEFAULT):
            self.value: VAL = value
        self.update()

