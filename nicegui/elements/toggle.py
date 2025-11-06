from typing import Generic, Optional, Union, overload
from typing_extensions import TypeVar

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from ..helpers import add_docstring_from
from .choice_element import ChoiceElement, Option, P, to_option
from .mixins.disableable_element import DisableableElement

V = TypeVar('V')


class Toggle(ChoiceElement[Optional[V], Option[P, V]], DisableableElement, Generic[V, P]):

    def __init__(self,
                 options: Union[list[P], dict[V, P]], *,
                 value: Optional[V] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments[Optional[V]]]] = None,
                 clearable: bool = False,
                 ) -> None:
        """Toggle

        This element is based on Quasar's `QBtnToggle <https://quasar.dev/vue-components/button-toggle>`_ component.

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param clearable: whether the toggle can be cleared by clicking the selected option
        """
        if isinstance(options, dict):
            super().__init__(tag='q-btn-toggle', options=[Option(v, k) for k, v in options.items()], value=value, on_change=on_change)
        else:
            super().__init__(tag='q-btn-toggle', options=[to_option(v) for v in options], value=value, on_change=on_change)
        self._props['clearable'] = clearable

    def _event_args_to_value(self, e: GenericEventArguments[Optional[V]]) -> Optional[V]:
        return e.args

    def _value_to_model_value(self, value: Optional[V]) -> Optional[V]:
        return value if value in self._values else None

@overload
def toggle(
    options: list[P], *,
    value: Optional[P] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[P]]]] = ...,
    clearable: bool = ...
) -> Toggle[P, P]:
    ...

@overload
def toggle(
    options: dict[V, P], *,
    value: Optional[V] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[P]]]] = ...,
    clearable: bool = ...
) -> Toggle[V, P]:
    ...

# pylint: disable=missing-function-docstring
@add_docstring_from(Toggle.__init__)
def toggle(
    options: Union[list[P], dict[V, P]], *,
    value: Optional[V] = None,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[V]]]] = None,
    clearable: bool = False
) -> Union[Toggle[V, P], Toggle[P, P]]:
    return Toggle(options, value=value, on_change=on_change, clearable=clearable)
