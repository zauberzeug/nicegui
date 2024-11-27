from typing import Any, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class Number(ValidationElement, DisableableElement):
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: Optional[float] = None,
                 min: Optional[float] = None,  # pylint: disable=redefined-builtin
                 max: Optional[float] = None,  # pylint: disable=redefined-builtin
                 precision: Optional[int] = None,
                 step: Optional[float] = None,
                 prefix: Optional[str] = None,
                 suffix: Optional[str] = None,
                 format: Optional[str] = None,  # pylint: disable=redefined-builtin
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        """Number Input

        This element is based on Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component.

        You can use the `validation` parameter to define a dictionary of validation rules,
        e.g. ``{'Too small!': lambda value: value > 3}``.
        The key of the first rule that fails will be displayed as an error message.
        Alternatively, you can pass a callable that returns an optional error message.
        To disable the automatic validation on every value change, you can use the `without_auto_validation` method.

        :param label: displayed name for the number input
        :param placeholder: text to show if no value is entered
        :param value: the initial value of the field
        :param min: the minimum value allowed
        :param max: the maximum value allowed
        :param precision: the number of decimal places allowed (default: no limit, negative: decimal places before the dot)
        :param step: the step size for the stepper buttons
        :param prefix: a prefix to prepend to the displayed value
        :param suffix: a suffix to append to the displayed value
        :param format: a string like "%.2f" to format the displayed value
        :param on_change: callback to execute when the value changes
        :param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)
        """
        self.format = format
        super().__init__(tag='q-input', value=value, on_value_change=on_change, validation=validation)
        self._props['type'] = 'number'
        if label is not None:
            self._props['label'] = label
        if placeholder is not None:
            self._props['placeholder'] = placeholder
        if min is not None:
            self._props['min'] = min
        if max is not None:
            self._props['max'] = max
        self._precision = precision
        if step is not None:
            self._props['step'] = step
        if prefix is not None:
            self._props['prefix'] = prefix
        if suffix is not None:
            self._props['suffix'] = suffix
        self.on('blur', self.sanitize, [])

    @property
    def min(self) -> float:
        """The minimum value allowed."""
        return self._props.get('min', -float('inf'))

    @min.setter
    def min(self, value: float) -> None:
        if self._props.get('min') == value:
            return
        self._props['min'] = value
        self.sanitize()
        self.update()

    @property
    def max(self) -> float:
        """The maximum value allowed."""
        return self._props.get('max', float('inf'))

    @max.setter
    def max(self, value: float) -> None:
        if self._props.get('max') == value:
            return
        self._props['max'] = value
        self.sanitize()
        self.update()

    @property
    def precision(self) -> Optional[int]:
        """The number of decimal places allowed (default: no limit, negative: decimal places before the dot)."""
        return self._precision

    @precision.setter
    def precision(self, value: Optional[int]) -> None:
        self._precision = value
        self.sanitize()

    @property
    def out_of_limits(self) -> bool:
        """Whether the current value is out of the allowed limits."""
        return not self.min <= self.value <= self.max

    def sanitize(self) -> None:
        """Sanitize the current value to be within the allowed limits."""
        if self.value is None:
            return
        value = float(self.value)
        value = max(value, self.min)
        value = min(value, self.max)
        if self.precision is not None:
            value = float(round(value, self.precision))
        self.set_value(float(self.format % value) if self.format else value)
        self.update()

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        if not e.args:
            return None
        return float(e.args)

    def _value_to_model_value(self, value: Any) -> Any:
        if value is None:
            return None
        if self.format is None:
            old_value = float(self._props.get(self.VALUE_PROP) or 0)
            if old_value == int(old_value) and value == int(value):
                return str(int(value))  # preserve integer representation
            return str(value)
        if value == '':
            return 0
        return self.format % float(value)
