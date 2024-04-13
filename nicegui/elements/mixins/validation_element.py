from typing import Any, Callable, Dict, Optional, Union

from typing_extensions import Self

from .value_element import ValueElement


class ValidationElement(ValueElement):

    def __init__(self, validation: Optional[Union[Callable[..., Optional[str]], Dict[str, Callable[..., bool]]]], **kwargs: Any) -> None:
        self.validation = validation if validation is not None else {}
        self._auto_validation = True
        self._error: Optional[str] = None
        super().__init__(**kwargs)

    @property
    def error(self) -> Optional[str]:
        """The latest error message from the validation functions."""
        return self._error

    @error.setter
    def error(self, error: Optional[str]) -> None:
        """Sets the error message.

        :param error: The optional error message
        """
        if self._error == error:
            return
        self._error = error
        self._props['error'] = error is not None
        self._props['error-message'] = error
        self.update()

    def validate(self) -> bool:
        """Validate the current value and set the error message if necessary.

        :return: True if the value is valid, False otherwise
        """
        if callable(self.validation):
            self.error = self.validation(self.value)
            return self.error is None

        for message, check in self.validation.items():
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
