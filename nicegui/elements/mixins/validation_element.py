from typing import Any, Callable, Dict, Optional, Union, Tuple, List

from .value_element import ValueElement


class ValidationElement(ValueElement):

    def __init__(self, validation: Union[List[Callable[..., Tuple[bool, str]]], Dict[str, Callable[..., bool]]], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.validation = validation
        self._error: Optional[str] = None

    @property
    def error(self) -> Optional[str]:
        """The latest error message from the validation functions."""
        return self._error

    def set_error_message(self, message: str) -> None:
        """Sets the error message.

        :param message: The error message
        """
        message = message.replace('\\', '\\\\')
        message = message.replace('\n', '<br>')
        message = message.replace('"', '\\"')
        self._error = message
        self.props(f'error error-message="{message}"')

    def clear_error_message(self) -> None:
        """Clears the error message."""
        self._error = None
        self.props(remove='error')

    def validate(self) -> None:
        """Validate the current value and set the error message if necessary."""
        if isinstance(self.validation, dict):
            for message, check in self.validation.items():
                if not check(self.value):
                    self.set_error_message(message)
                    return
        else:
            for check in self.validation:
                ret, message = check(self.value)
                if not ret:
                    self.set_error_message(message)
                    return
        self.clear_error_message()

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        self.validate()
