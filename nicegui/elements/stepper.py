from __future__ import annotations

from typing import Any, Callable, Optional, Union

from .. import globals
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Stepper(ValueElement):

    def __init__(self, *,
                 value: Union[str, Step, None] = None,
                 on_value_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        super().__init__(tag='q-stepper', value=value, on_value_change=on_value_change)

    def _value_to_model_value(self, value: Any) -> Any:
        return value._props['name'] if isinstance(value, Step) else value


class Step(DisableableElement):

    def __init__(self, name: str, title: Optional[str] = None, icon: Optional[str] = None) -> None:
        super().__init__(tag='q-step')
        self._props['name'] = name
        self._props['title'] = title if title is not None else name
        if icon:
            self._props['icon'] = icon
        self.stepper = globals.get_slot().parent
