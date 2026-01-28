from typing import Any, Literal, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class InputChips(LabelElement, ValidationElement, DisableableElement):

    def __init__(self,
                 label: Optional[str] = None,
                 *,
                 value: Optional[list[str]] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 new_value_mode: Literal['add', 'add-unique', 'toggle'] = 'toggle',
                 clearable: bool = False,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        """Input Chips

        An input field that manages a collection of values as visual "chips" or tags.
        Users can type to add new chips and remove existing ones by clicking or using keyboard shortcuts.
        Values are added by pressing Enter or when the input field loses focus (blur event).

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

        self._props['new-value-mode'] = new_value_mode
        self._props['use-input'] = True
        self._props['use-chips'] = True
        self._props['fill-input'] = True
        self._props['input-debounce'] = 0
        self._props['multiple'] = True
        self._props['hide-dropdown-icon'] = True
        self._props['clearable'] = clearable

        # Track the current input value to add on blur
        self._current_input_value = ''
        self._new_value_mode = new_value_mode

        # Listen to input-value changes to track what user is typing
        self.on('input-value', self._handle_input_value_change)

        # Listen to blur event to add the current input value as a chip
        self.on('blur', self._handle_blur)

    def _handle_input_value_change(self, e: GenericEventArguments) -> None:
        """Track the current input value as user types."""
        self._current_input_value = e.args if e.args else ''

    def _handle_blur(self, e: GenericEventArguments) -> None:
        """Add the current input value as a chip when field loses focus."""
        val = self._current_input_value.strip() if isinstance(self._current_input_value, str) else ''

        if not val:
            return

        # Get current chips
        current_value = self.value if self.value else []

        # Apply new-value-mode logic
        if self._new_value_mode == 'add':
            # Always add the value
            new_value = current_value + [val]
        elif self._new_value_mode == 'add-unique':
            # Only add if not already present
            if val not in current_value:
                new_value = current_value + [val]
            else:
                return
        elif self._new_value_mode == 'toggle':
            # Toggle: add if not present, remove if present
            if val in current_value:
                new_value = [v for v in current_value if v != val]
            else:
                new_value = current_value + [val]
        else:
            return

        # Update the value
        self.value = new_value

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        return e.args or []
