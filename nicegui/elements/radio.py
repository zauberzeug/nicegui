from typing import Any, Generic, Optional, Union, overload
from typing_extensions import TypeVar

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from ..helpers import add_docstring_from
from .choice_element import ChoiceElement, Option, P, to_option
from .mixins.disableable_element import DisableableElement

V = TypeVar('V')


class Radio(ChoiceElement[Optional[V], Option[P, V]], DisableableElement, Generic[V, P]):

    def __init__(self,
                 options: Union[list[P], dict[V, P]], *,
                 value: Optional[V] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments[Optional[V]]]] = None,
                 ) -> None:
        """Radio Selection

        This element is based on Quasar's `QOptionGroup <https://quasar.dev/vue-components/option-group>`_ component.

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        """
        if isinstance(options, dict):
            super().__init__(tag='q-option-group', options=[Option(v, k) for k, v in options.items()], value=value, on_change=on_change)
        else:
            super().__init__(tag='q-option-group', options=[to_option(v) for v in options], value=value, on_change=on_change)

    def _event_args_to_value(self, e: GenericEventArguments[Optional[V]]) -> Any:
        return e.args

    def _value_to_model_value(self, value: Optional[V]) -> Optional[V]:
        return value if value in self._values else None


@overload
def radio(
    options: list[P], *,
    value: Optional[P] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[P]]]] = ...,
) -> Radio[P, P]:
    ...

@overload
def radio(
    options: dict[V, P], *,
    value: Optional[V] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[V]]]] = ...,
) -> Radio[V, P]:
    ...

# pylint: disable=missing-function-docstring
@add_docstring_from(Radio.__init__)
def radio(
    options: Union[list[P], dict[V, P]], *,
    value: Optional[V] = None,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[V]]]] = None,
) -> Union[Radio[V, P], Radio[P, P]]:
    return Radio(options, value=value, on_change=on_change)

