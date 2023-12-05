from typing import Any, Callable, Dict, Optional, Union, Tuple, List

from .value_element import ValueElement


class ValidationElement(ValueElement):

    def __init__(self, validation: Union[List[Callable[..., Tuple[bool, str]]], Dict[str, Callable[..., bool]]], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.validation = validation
        self._error: Optional[str] = None
        self._validate_individually = False

    @property
    def error(self) -> Optional[str]:
        """The latest error message from the validation functions."""
        return self._error

    @error.setter
    def error(self, error: Optional[str]) -> None:
        """The setter for an error.

        :param error: Optional error message
        """
        self._error = error

    def set_validate_individually(self, value: bool) -> None:
        """Sets whether or not the validate value elements individually.

        :param value: Whether or not to evaluate value elements individually
        """
        self._validate_individually = value

    def _set_error_message(self, message: str) -> None:
        """Sets the error message.

        :param message: The error message
        """
        message = message.replace('"', '\\"')
        self._error = message
        self.props(f'error error-message="{message}"')

    def _clear_error_message(self) -> None:
        """Clears the error message."""
        self._error = None
        self.props(remove='error')

    def _validate_single_value(self, value: Any) -> bool:
        """Validates single value element and sets the error message if necessary.

        :param value: The single value element
        :return: True if given single value element is valid, otherwise false
        :rtype: bool
        """
        if isinstance(self.validation, dict):
            for message, check in self.validation.items():
                if not check(self.value):
                    self._set_error_message(message)
                    return False
        else:
            for check in self.validation:
                ret, message = check(value)
                if not ret:
                    self._set_error_message(message)
                    return False
        return True

    def validate(self) -> None:
        """Validate the current value and set the error message if necessary."""
        if self._validate_individually and isinstance(self.value, list):
            for value in self.value:
                if not self._validate_single_value(value):
                    return
        elif not self._validate_single_value(self.value):
            return
        self._clear_error_message()

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        self.validate()
