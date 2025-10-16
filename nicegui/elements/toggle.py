from collections.abc import Collection
from typing import Any, Optional

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import ChoiceElement, T
from .mixins.disableable_element import DisableableElement


class Toggle(ChoiceElement[T], DisableableElement):

    def __init__(self,
                 options: Collection[T], *,
                 value: tuple[T, ...] = (),
                 on_change: Optional[Handler[ValueChangeEventArguments[tuple[T, ...]]]] = None,
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
        super().__init__(tag='q-btn-toggle', options=options, value=value, on_change=on_change, js_handler='(_, option) => emit(option)')
        self._props['clearable'] = clearable

    def _event_args_to_value(self, e: GenericEventArguments[Optional[dict[Any, Any]]]) -> tuple[T, ...]:
        return (self._index_to_option[e.args['id']],) if e.args else ()

    def _value_to_model_value(self, value: tuple[T, ...]) -> str:
        vals = tuple(v for v in value if v in self.options)
        return vals[0].value if vals else ''
