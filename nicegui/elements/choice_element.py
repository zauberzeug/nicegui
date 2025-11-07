import hashlib
from dataclasses import dataclass
from typing import Any, Generic, Optional, Union, overload, Iterable  # pylint: disable=unused-import

# NOTE: pylint ignore is for the `Any` import.
from typing_extensions import TypedDict, TypeVar

from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement

JsonPrimitive = Union[str, int, float, bool, None]
P = TypeVar('P', bound=JsonPrimitive)
V = TypeVar('V')
T = TypeVar('T', bound='Option[Any, Any]')

class DEFAULT:
    pass

default = DEFAULT()
# ^ used as default value in set_options below

@dataclass
class Option(Generic[P, V]):
    label: P
    value: V

    def __post_init__(self) -> None:
        self.id = hashlib.md5(f'{self.label}{self.value}'.encode()).hexdigest()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.label}, {self.value})"

    def __repr__(self) -> str:
        return self.__str__()


class OptionDict(TypedDict, Generic[P, V]):
    label: P
    value: V
    id: str


@overload
def to_option(v: P) -> Option[P, P]:
    ...

@overload
def to_option(v: Option[P, V]) -> Option[P, V]:
    ...

def to_option(v: Union[P, Option[P, V]]) -> Union[Option[P, V], Option[P, P]]:
    """Converts a primitive type to an `Option`. If the value is already an `Option`, it will return that option unchanged.

    :param v: The primitive type (`int`, `float`, `str`, `bool`, `None`)
    """
    if isinstance(v, Option):
        return v
    return Option(label=v, value=v)


class ChoiceElement(ValueElement[V], Generic[V, T]):

    def __init__(self, *,
                 tag: Optional[str] = None,
                 options: Iterable[T],
                 value: V,
                 on_change: Optional[Handler[ValueChangeEventArguments[V]]] = None,
                 ) -> None:
        self.value = value
        self.options = list(options)
        self._values = [o.value for o in self.options]
        self._labels = [o.label for o in self.options]
        self._id_to_option = {o.id: o for o in self.options}
        if (invalid_values := self._invalid_values(value)):
            raise ValueError(f'Invalid values: {invalid_values}')
        super().__init__(tag=tag, value=value, on_value_change=on_change)
        self._update_options()

    def _invalid_values(self, value: V) -> tuple[V, ...]:
        if value is None:
            return tuple()
        return tuple(set([value]) - set(self._values))

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

    def set_options(self, options: Iterable[T], *, value: Union[V, DEFAULT] = default) -> None:
        """Set the options of this choice element.

        :param options: The new options.
        :param value: The new value. If not given, the current value is kept.
        """
        self.options = list(options)
        if not isinstance(value, DEFAULT):
            self.value: V = value
        self.update()
