from typing import Any, Optional, Iterable

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import ChoiceElement, Option, P, to_option
from .mixins.disableable_element import DisableableElement


class Radio(ChoiceElement[Optional[P], Option[P, P]], DisableableElement):

    def __init__(self,
                 options: Iterable[P], *,
                 value: Any = None,
                 on_change: Optional[Handler[ValueChangeEventArguments[Optional[P]]]] = None,
                 ) -> None:
        """Radio Selection

        This element is based on Quasar's `QOptionGroup <https://quasar.dev/vue-components/option-group>`_ component.

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        """
        super().__init__(tag='q-option-group', options=[to_option(v) for v in options], value=value, on_change=on_change)

    def _event_args_to_value(self, e: GenericEventArguments[Optional[P]]) -> Any:
        return e.args

    def _value_to_model_value(self, value: Optional[P]) -> Optional[P]:
        return value if value in self._values else None
