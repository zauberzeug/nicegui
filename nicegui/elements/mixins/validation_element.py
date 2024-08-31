from typing import Any, Callable, Dict, Optional, Union

from typing_extensions import Self

from .value_element import ValueElement


class ValidationElement(ValueElement):

    def __init__(self, validation: Optional[Union[Callable[..., Optional[str]], Dict[str, Callable[..., bool]]]], **kwargs: Any) -> None:
        self._validation = validation
        self._auto_validation = True
        self._error: Optional[str] = None
        super().__init__(**kwargs)
        self._props['error'] = None if validation is None else False  # NOTE: reserve bottom space for error message

    @property
    def validation(self) -> Optional[Union[Callable[..., Optional[str]], Dict[str, Callable[..., bool]]]]:
        """The validation function or dictionary of validation functions."""
        return self._validation

    @validation.setter
    def validation(self, validation: Optional[Union[Callable[..., Optional[str]], Dict[str, Callable[..., bool]]]]) -> None:
        """Sets the validation function or dictionary of validation functions.

        :param validation: validation function or dictionary of validation functions (``None`` to disable validation)
        """
        self._validation = validation
        self.validate()

    @property
    def error(self) -> Optional[str]:
        """The latest error message from the validation functions."""
        return self._error

    @error.setter
    def error(self, error: Optional[str]) -> None:
        """Sets the error message.

        :param error: The optional error message
        """
        new_error_prop = None if self.validation is None else (error is not None)
        if self._error == error and self._props['error'] == new_error_prop:
            return
        self._error = error
        self._props['error'] = new_error_prop
        self._props['error-message'] = error
        self.update()

    def validate(self) -> bool:
        """Validate the current value and set the error message if necessary.

        :return: True if the value is valid, False otherwise
        """
        if callable(self._validation):
            self.error = self._validation(self.value)
            return self.error is None

        if isinstance(self._validation, dict):
            for message, check in self._validation.items():
                if not check(self.value):
                    self.error = message
                    return False

        self.error = None
        return True

    def without_auto_validation(self) -> Self:
        """Disable automatic validation on value change."""
        self._auto_validation = False
        return self

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if self._auto_validation:
            self.validate()
