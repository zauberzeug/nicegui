from typing import Any, Literal

from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class InputChips(LabelElement, ValidationElement, DisableableElement):

    @resolve_defaults
    def __init__(self,
                 label: str | None = DEFAULT_PROP | None,
                 *,
                 value: list[str] | None = DEFAULT_PROPS['model-value'] | None,
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 new_value_mode: Literal['add', 'add-unique', 'toggle'] = DEFAULT_PROP | 'toggle',
                 clearable: bool = DEFAULT_PROP | False,
                 validation: ValidationFunction | ValidationDict | None = None,
                 ) -> None:
        """Input Chips

        An input field that manages a collection of values as visual "chips" or tags.
        Users can type to add new chips and remove existing ones by clicking or using keyboard shortcuts.

        This element is based on Quasar's `QSelect <https://quasar.dev/vue-components/select>`_ component.
        Unlike a traditional dropdown selection, this variant focuses on free-form text input with chips,
        making it ideal for tags, keywords, or any list of user-defined values.

        You can use the ``validation`` parameter to define a dictionary of validation rules,
        e.g. ``{'Too long!': lambda value: len(value) < 3}``.
        The key of the first rule that fails will be displayed as an error message.
        Alternatively, you can pass a callable that returns an optional error message.
        To disable the automatic validation on every value change, you can use the `without_auto_validation` method.

        *Added in version 2.22.0*

        :param label: the label to display above the selection
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param new_value_mode: handle new values from user input (default: "toggle")
        :param clearable: whether to add a button to clear the selection
        :param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)
        """
        super().__init__(tag='q-select', label=label, value=value or [], on_value_change=on_change, validation=validation)

        self._props['for'] = self.html_id
        self._props['new-value-mode'] = new_value_mode
        self._props['use-input'] = True
        self._props['use-chips'] = True
        self._props['fill-input'] = True
        self._props['input-debounce'] = 0
        self._props['multiple'] = True
        self._props['hide-dropdown-icon'] = True
        self._props['clearable'] = clearable

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        return e.args or []
