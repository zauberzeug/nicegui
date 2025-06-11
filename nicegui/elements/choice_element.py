from typing import Any, Collection, Generic, Hashable, Optional, Union

from packaging.version import Version
from typing_extensions import TypeVar

from ..events import Handler, ValueChangeEventArguments
from ..helpers import PYTHON_VERSION
from .mixins.value_element import ValueElement

if PYTHON_VERSION > Version("3.11"):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

T = TypeVar("T", bound=Hashable, default=str)
LT = TypeVar("LT", bound=Hashable, default=str)
VT = TypeVar("VT", default=str)


class Option(TypedDict, Generic[LT, VT]):
    label: LT
    value: VT


def _to_option(value: Union[Option, str]) -> Option:
    if not isinstance(value, dict):
        return Option(label=value, value=value)
    return value


class ChoiceElement(ValueElement, Generic[LT, VT]):

    def __init__(self, *,
                 tag: Optional[str] = None,
                 options: Collection[Union[Option[LT, VT], VT]],
                 value: VT,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        self.options: list[Option[LT, VT]] = [_to_option(v) for v in options]
        self._values: list[VT] = []
        self._labels: list[LT] = []
        self._values_to_option: dict[VT, Option[LT, VT]] = {
            o["value"]: o for o in self.options
        }
        self._update_values_and_labels()
        if not isinstance(value, list) and value is not None and value not in self._values:
            raise ValueError(f'Invalid value: {value}')
        super().__init__(tag=tag, value=value, on_value_change=on_change)
        self._update_options()

    def _update_values_and_labels(self) -> None:
        self._values = [o["value"] for o in self.options]
        self._labels = [o["label"] for o in self.options]
        self._values_to_option: dict[VT, Option[LT, VT]] = {
            o["value"]: o for o in self.options
        }

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = self.options
        self._props[self.VALUE_PROP] = self._value_to_model_value(before_value)
        if not isinstance(before_value, list):  # NOTE: no need to update value in case of multi-select
            self.value: Optional[VT] = before_value if before_value in self._values else None

    def update(self) -> None:
        with self._props.suspend_updates():
            self._update_values_and_labels()
            self._update_options()
        super().update()

    def set_options(self, options: Collection[Option | str], *, value: Any = ...) -> None:
        """Set the options of this choice element.

        :param options: The new options.
        :param value: The new value. If not given, the current value is kept.
        """
        self.options = [_to_option(v) for v in options]
        if value is not ...:
            self.value = value
        self.update()
