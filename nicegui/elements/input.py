from typing import Any, List, Optional, Union

from ..events import Handler, ValueChangeEventArguments
from .icon import Icon
from .mixins.disableable_element import DisableableElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class Input(ValidationElement, DisableableElement, component='input.js'):
    VALUE_PROP: str = 'value'
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 password: bool = False,
                 password_toggle_button: bool = False,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 autocomplete: Optional[List[str]] = None,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        """Text Input

        This element is based on Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component.

        The `on_change` event is called on every keystroke and the value updates accordingly.
        If you want to wait until the user confirms the input, you can register a custom event callback, e.g.
        `ui.input(...).on('keydown.enter', ...)` or `ui.input(...).on('blur', ...)`.

        You can use the `validation` parameter to define a dictionary of validation rules,
        e.g. ``{'Too long!': lambda value: len(value) < 3}``.
        The key of the first rule that fails will be displayed as an error message.
        Alternatively, you can pass a callable that returns an optional error message.
        To disable the automatic validation on every value change, you can use the `without_auto_validation` method.

        Note about styling the input:
        Quasar's `QInput` component is a wrapper around a native `input` element.
        This means that you cannot style the input directly,
        but you can use the `input-class` and `input-style` props to style the native input element.
        See the "Style" props section on the `QInput <https://quasar.dev/vue-components/input>`_ documentation for more details.

        :param label: displayed label for the text input
        :param placeholder: text to show if no value is entered
        :param value: the current value of the text input
        :param password: whether to hide the input (default: False)
        :param password_toggle_button: whether to show a button to toggle the password visibility (default: False)
        :param on_change: callback to execute when the value changes
        :param autocomplete: optional list of strings for autocompletion
        :param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)
        """
        super().__init__(value=value, on_value_change=on_change, validation=validation)
        if label is not None:
            self._props['label'] = label
        if placeholder is not None:
            self._props['placeholder'] = placeholder
        self._props['type'] = 'password' if password else 'text'

        if password_toggle_button:
            with self.add_slot('append'):
                def toggle_type(_):
                    is_hidden = self._props.get('type') == 'password'
                    icon.props(f'name={"visibility" if is_hidden else "visibility_off"}')
                    self.props(f'type={"text" if is_hidden else "password"}')
                icon = Icon('visibility_off').classes('cursor-pointer').on('click', toggle_type)

        self._props['_autocomplete'] = autocomplete or []

    def set_autocomplete(self, autocomplete: Optional[List[str]]) -> None:
        """Set the autocomplete list."""
        self._props['_autocomplete'] = autocomplete
        self.update()

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if self._send_update_on_value_change:
            self.run_method('updateValue')
