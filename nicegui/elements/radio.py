from typing import Any

from ..defaults import DEFAULT_PROPS, resolve_defaults
from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import ChoiceElement
from .mixins.disableable_element import DisableableElement


class Radio(ChoiceElement, DisableableElement):

    @resolve_defaults
    def __init__(self,
                 options: list | dict, *,
                 value: Any = DEFAULT_PROPS['model-value'] | None,
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Radio Selection

        This element is based on Quasar's `QOptionGroup <https://quasar.dev/vue-components/option-group>`_ component.

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        """
        super().__init__(tag='q-option-group', options=options, value=value, on_change=on_change)

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        return self._values[e.args]

    def _value_to_model_value(self, value: Any) -> Any:
        return self._values.index(value) if value in self._values else None
