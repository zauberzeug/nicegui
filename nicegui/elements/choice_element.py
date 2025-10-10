from typing import Any, Collection, Generic, Optional, Union

from packaging.version import Version
from typing_extensions import TypeVar

from ..events import Handler, ValueChangeEventArguments
from ..helpers import PYTHON_VERSION
from .mixins.value_element import ValueElement

if PYTHON_VERSION > Version("3.11"):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


LT = TypeVar("LT")
VT = TypeVar("VT")
T = TypeVar("T", bound="Option[Any, Any]")


class Option(TypedDict, Generic[LT, VT]):
    label: LT
    value: VT


class ChoiceElement(ValueElement[Optional[Union[list[T], T]]], Generic[T]):

    def __init__(self, *,
                 tag: Optional[str] = None,
                 options: list[T],
                 value: Optional[Union[list[T], T]] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        self.options = options
        self._update_values_and_labels()
        if value and not isinstance(value, list) and value["value"] not in [o["value"] for o in options]:
            raise ValueError(f'Invalid values: {value}')
        if value and isinstance(value, list) and (invalid_values := set(o["value"] for o in value) - set(o["value"] for o in options)):
            raise ValueError(f'Invalid values: {invalid_values}')
        super().__init__(tag=tag, value=value, on_value_change=on_change)
        self._update_options()

    def _update_values_and_labels(self) -> None:
        self._values = [o["value"] for o in self.options]
        self._labels = [o["label"] for o in self.options]

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = self.options
        self._props[self.VALUE_PROP] = self._value_to_model_value(before_value)

    def update(self) -> None:
        with self._props.suspend_updates():
            self._update_values_and_labels()
            self._update_options()
        super().update()

    def set_options(self, options: list[T], *, value: Optional[Union[list[T], T]] = None) -> None:
        """Set the options of this choice element.

        :param options: The new options.
        :param value: The new value. If not given, the current value is kept.
        """
        self.options = list(options)
        if value:
            self.value = value
        self.update()

