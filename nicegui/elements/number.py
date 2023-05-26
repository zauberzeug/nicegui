from typing import Any, Callable, Dict, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Number(ValueElement, DisableableElement):
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: Optional[float] = None,
                 min: Optional[float] = None,
                 max: Optional[float] = None,
                 step: Optional[float] = None,
                 prefix: Optional[str] = None,
                 suffix: Optional[str] = None,
                 format: Optional[str] = None,
                 on_change: Optional[Callable[..., Any]] = None,
                 validation: Dict[str, Callable[..., bool]] = {},
                 ) -> None:
        """Number Input

        This element is based on Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component.

        You can use the `validation` parameter to define a dictionary of validation rules.
        The key of the first rule that fails will be displayed as an error message.

        :param label: displayed name for the number input
        :param placeholder: text to show if no value is entered
        :param value: the initial value of the field
        :param min: the minimum value allowed
        :param max: the maximum value allowed
        :param step: the step size for the stepper buttons
        :param prefix: a prefix to prepend to the displayed value
        :param suffix: a suffix to append to the displayed value
        :param format: a string like "%.2f" to format the displayed value
        :param on_change: callback to execute when the value changes
        :param validation: dictionary of validation rules, e.g. ``{'Too small!': lambda value: value < 3}``
        """
        self.format = format
        super().__init__(tag='q-input', value=value, on_value_change=on_change)
        self._props['type'] = 'number'
        if label is not None:
            self._props['label'] = label
        if placeholder is not None:
            self._props['placeholder'] = placeholder
        if min is not None:
            self._props['min'] = min
        if max is not None:
            self._props['max'] = max
        if step is not None:
            self._props['step'] = step
        if prefix is not None:
            self._props['prefix'] = prefix
        if suffix is not None:
            self._props['suffix'] = suffix
        self.validation = validation
        self.on('blur', self.sanitize)

    def sanitize(self) -> None:
        value = float(self.value or 0)
        value = max(value, self._props.get('min', -float('inf')))
        value = min(value, self._props.get('max', float('inf')))
        self.set_value(float(self.format % value) if self.format else value)

    def on_value_change(self, value: Any) -> None:
        super().on_value_change(value)
        for message, check in self.validation.items():
            if not check(value):
                self.props(f'error error-message="{message}"')
                break
        else:
            self.props(remove='error')

    def _msg_to_value(self, msg: Dict) -> Any:
        return float(msg['args']) if msg['args'] else None

    def _value_to_model_value(self, value: Any) -> Any:
        if value is None:
            return None
        elif self.format is None:
            return str(value)
        elif value == '':
            return 0
        else:
            return self.format % float(value)

    def _value_to_event_value(self, value: Any) -> Any:
        return float(value) if value else 0
