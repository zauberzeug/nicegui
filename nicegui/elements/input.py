from typing import Any, Callable, Dict, Optional

from .icon import Icon
from .mixins.value_element import ValueElement


class Input(ValueElement):
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 password: bool = False,
                 password_toggle_button: bool = False,
                 on_change: Optional[Callable] = None,
                 validation: Dict[str, Callable] = {}) -> None:
        """Text Input

        This element is based on Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component.

        The `on_change` event is called on every keystroke and the value updates accordingly.
        If you want to wait until the user confirms the input, you can register a custom event callback, e.g.
        `ui.input(...).on('keydown.enter', ...)` or `ui.input(...).on('blur', ...)`.

        You can use the `validation` parameter to define a dictionary of validation rules.
        The key of the first rule that fails will be displayed as an error message.

        :param label: displayed label for the text input
        :param placeholder: text to show if no value is entered
        :param value: the current value of the text input
        :param password: whether to hide the input (default: False)
        :param password_toggle_button: whether to show a button to toggle the password visibility (default: False)
        :param on_change: callback to execute when the input is confirmed by leaving the focus
        :param validation: dictionary of validation rules, e.g. ``{'Too short!': lambda value: len(value) < 3}``
        """
        super().__init__(tag='q-input', value=value, on_value_change=on_change)
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

        self.validation = validation

    def on_value_change(self, value: Any) -> None:
        super().on_value_change(value)
        for message, check in self.validation.items():
            if not check(value):
                self.props(f'error error-message="{message}"')
                break
        else:
            self.props(remove='error')
