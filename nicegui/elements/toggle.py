from collections.abc import Iterable
from typing import Optional

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import ChoiceElement, Option, P, to_option
from .mixins.disableable_element import DisableableElement


class Toggle(ChoiceElement[Optional[P], Option[P, P]], DisableableElement):

    def __init__(self,
                 options: Iterable[P], *,
                 value: Optional[P] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments[Optional[P]]]] = None,
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
        super().__init__(tag='q-btn-toggle', options=[to_option(v) for v in options], value=value, on_change=on_change)
        self._props['clearable'] = clearable

    def _event_args_to_value(self, e: GenericEventArguments[Optional[P]]) -> Optional[P]:
        return e.args

    def _value_to_model_value(self, value: Optional[P]) -> Optional[P]:
        return value if value in self._values else None
