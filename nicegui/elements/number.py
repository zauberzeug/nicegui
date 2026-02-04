from typing import Any

from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class Number(LabelElement, ValidationElement, DisableableElement):
    LOOPBACK = False

    @resolve_defaults
    def __init__(self,
                 label: str | None = DEFAULT_PROP | None, *,
                 placeholder: str | None = DEFAULT_PROP | None,
                 value: float | None = DEFAULT_PROPS['model-value'] | None,
                 min: float | None = DEFAULT_PROP | None,  # pylint: disable=redefined-builtin
                 max: float | None = DEFAULT_PROP | None,  # pylint: disable=redefined-builtin
                 precision: int | None = None,
                 step: float | None = DEFAULT_PROP | None,
                 prefix: str | None = DEFAULT_PROP | None,
                 suffix: str | None = DEFAULT_PROP | None,
                 format: str | None = None,  # pylint: disable=redefined-builtin
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 validation: ValidationFunction | ValidationDict | None = None,
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
        super().__init__(tag='q-input', label=label, value=value, on_value_change=on_change, validation=validation)
        self._props['for'] = self.html_id
        self._props['type'] = 'number'
        self._props.set_optional('placeholder', placeholder)
        self._props.set_optional('min', min)
        self._props.set_optional('max', max)
        self._precision = precision
        self._props.set_optional('step', step)
        self._props.set_optional('prefix', prefix)
        self._props.set_optional('suffix', suffix)
        self.on('blur', self.sanitize, [])

    @property
    def min(self) -> float:
        """The minimum value allowed."""
        return self._props.get('min', -float('inf'))

    @min.setter
    def min(self, value: float) -> None:
        if self._props.get('min') == value:
            return
        self._props.set_optional('min', value)
        self.sanitize()

    @property
    def max(self) -> float:
        """The maximum value allowed."""
        return self._props.get('max', float('inf'))

    @max.setter
    def max(self, value: float) -> None:
        if self._props.get('max') == value:
            return
        self._props.set_optional('max', value)
        self.sanitize()

    @property
    def precision(self) -> int | None:
        """The number of decimal places allowed (default: no limit, negative: decimal places before the dot)."""
        return self._precision

    @precision.setter
    def precision(self, value: int | None) -> None:
        self._precision = value
        self.sanitize()

    @property
    def prefix(self) -> str | None:
        """The prefix to prepend to the displayed value.

        *Added in version 3.5.0*
        """
        return self._props.get('prefix')

    @prefix.setter
    def prefix(self, value: str | None) -> None:
        if value is None:
            self._props.pop('prefix', None)
        else:
            self._props['prefix'] = value

    @property
    def suffix(self) -> str | None:
        """The suffix to append to the displayed value.

        *Added in version 3.5.0*
        """
        return self._props.get('suffix')

    @suffix.setter
    def suffix(self, value: str | None) -> None:
        if value is None:
            self._props.pop('suffix', None)
        else:
            self._props['suffix'] = value

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
        self.value = float(self.format % value) if self.format else value
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
