from collections.abc import Callable
from typing import Any, Generic

from ..defaults import DEFAULT_PROPS, resolve_defaults
from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import ChoiceElement, OptionT
from .mixins.disableable_element import DisableableElement


class Radio(ChoiceElement[OptionT, 'OptionT | None'], DisableableElement, Generic[OptionT]):

    @resolve_defaults
    def __init__(self,
                 options: list[OptionT] | dict[OptionT, Any], *,
                 value: OptionT | None = DEFAULT_PROPS['model-value'] | None,
                 on_change: Handler[ValueChangeEventArguments[OptionT | None]] | None = None,
                 option_label: Callable[[OptionT], Any] | None = None,
                 ) -> None:
        """Radio Selection

        This element is based on Quasar's `QOptionGroup <https://quasar.dev/vue-components/option-group>`_ component.

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param option_label: a callback mapping an option to the label shown for it (default: None, i.e. the option itself)
        """
        super().__init__(tag='q-option-group', options=options, value=value, on_change=on_change,
                         option_label=option_label)

    def _event_args_to_value(self, e: GenericEventArguments) -> OptionT | None:
        return self._values[e.args]

    def _value_to_model_value(self, value: Any) -> Any:
        return self._values.index(value) if value in self._values else None
