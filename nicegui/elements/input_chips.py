from typing import Any, List, Literal, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class InputChips(LabelElement, ValidationElement, DisableableElement):

    def __init__(self,
                 value: Any = None,
                 *,
                 label: Optional[str] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 new_value_mode: Literal['add', 'add-unique', 'toggle'] = 'toggle',
                 clearable: bool = False,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        """Input Chips

        This element is based on Quasar's `QSelect <https://quasar.dev/vue-components/select>`_ component.
        This variant of select focuses solely on using chips without dropdown menu which is suitable for longer lists.
        Hence, it acts as an input with list of chips rather than a dropdown of choices.

        You can use the `validation` parameter to define a dictionary of validation rules,
        e.g. ``{'Too long!': lambda value: len(value) < 3}``.
        The key of the first rule that fails will be displayed as an error message.
        Alternatively, you can pass a callable that returns an optional error message.
        To disable the automatic validation on every value change, you can use the `without_auto_validation` method.

        :param value: the initial value
        :param label: the label to display above the selection
        :param on_change: callback to execute when selection changes
        :param new_value_mode: handle new values from user input (default: "toggle")
        :param clearable: whether to add a button to clear the selection
        :param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)
        """
        if value is None:
            value = []
        elif not isinstance(value, list):
            value = [value]

        super().__init__(tag='q-select', label=label, value=value, on_value_change=on_change, validation=validation)

        self._props['new-value-mode'] = new_value_mode
        self._props['use-input'] = True
        self._props['use-chips'] = True
        self._props['fill-input'] = True
        self._props['input-debounce'] = 0
        self._props['multiple'] = True
        self._props['hide-dropdown-icon'] = True
        self._props['clearable'] = clearable

        self.new_value: List[str] = []
        self._old_values: List[str] = value

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        self.new_value = [val for val in e.args if val not in self._old_values]
        self._old_values = e.args
        return e.args or []

    def get_new_value(self):
        """Returns the new value is typed in or None."""
        return None if len(self.new_value) == 0 else self.new_value[0]

    def append_values(self, values: Union[List[str], str]):
        """Appends the value or list of values according to the configured `new_value_mode`."""
        new_value_mode = self._props['new-value-mode']
        if not isinstance(values, list):
            values = [values]
        for value in values:
            if new_value_mode == 'add':
                self.value.append(value)
            elif value not in self.value:
                self.value.append(value)
            elif new_value_mode == 'toggle':
                self.value.remove(value)
