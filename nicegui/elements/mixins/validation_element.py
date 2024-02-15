from typing import Any, Callable, Dict, Optional, Union

from .value_element import ValueElement


class ValidationElement(ValueElement):
    """
    A mixin class for adding validation functionality to an element.

    This mixin provides methods and properties for validating the current value of an element
    and setting an error message if necessary. It can be used as a base class for creating
    custom elements that require validation.

    Args:
    - validation: Optional validation function or dictionary of validation functions.
                       If a function is provided, it should take the current value as an argument
                       and return an optional error message. If a dictionary is provided, the keys
                       should be error messages and the values should be validation functions that
                       take the current value as an argument and return a boolean indicating whether
                       the value is valid.
    - kwargs: Additional keyword arguments to be passed to the base class constructor.

    Example usage:

    ```python
    class MyElement(ValidationElement):
        def __init__(self, **kwargs):
            super().__init__(validation=self.validate_value, **kwargs)

        def validate_value(self, value):
            if value < 0:
                return "Value must be positive."
            return None
    ```

    The `ValidationElement` class provides the following methods and properties:

    Methods:
    - validate(): Validate the current value and set the error message if necessary.
                  Returns True if the value is valid, False otherwise.

    Properties:
    - error: The latest error message from the validation functions.
             Setting this property will update the error state of the element.

    """

    def __init__(self, validation: Optional[Union[Callable[..., Optional[str]], Dict[str, Callable[..., bool]]]], **kwargs: Any) -> None:
        """
        Initialize a ValidationElement object.

        Args:
            validation (Optional[Union[Callable[..., Optional[str]], Dict[str, Callable[..., bool]]]]): 
                A validation function or a dictionary of validation functions.
                If a validation function is provided, it should take the form of `Callable[..., Optional[str]]`,
                where the arguments are the values to be validated and the return value is an optional error message.
                If a dictionary of validation functions is provided, it should have string keys representing the 
                validation names and values as the corresponding validation functions.
            **kwargs (Any): Additional keyword arguments to be passed to the parent class constructor.

        Returns:
            None

        Raises:
            None

        Example usage:
            # Create a ValidationElement with a single validation function
            def validate_length(value: str) -> Optional[str]:
                if len(value) < 5:
                    return "Value must be at least 5 characters long."
                return None

            element = ValidationElement(validation=validate_length)

            # Create a ValidationElement with multiple validation functions
            def validate_length(value: str) -> Optional[str]:
                if len(value) < 5:
                    return "Value must be at least 5 characters long."
                return None

            def validate_numeric(value: str) -> Optional[str]:
                if not value.isnumeric():
                    return "Value must be numeric."
                return None

            element = ValidationElement(validation={
                'length': validate_length,
                'numeric': validate_numeric
            })
        """
        super().__init__(**kwargs)
        self.validation = validation if validation is not None else {}
        self._error: Optional[str] = None

    @property
    def error(self) -> Optional[str]:
        """
        Returns the latest error message from the validation functions.

        Return:
            The latest error message as a string, or None if there is no error.
            :type: Optional[str]
        """
        return self._error

    @error.setter
    def error(self, error: Optional[str]) -> None:
        """Sets the error message.

        This method sets the error message for the validation element. The error message
        is displayed when the element fails validation.

        Args:
        - error: The optional error message to be set. If None, the error message
                      will be cleared.
        :type error: str or None
        """
        if self._error == error:
            return
        self._error = error
        self._props['error'] = error is not None
        self._props['error-message'] = error
        self.update()

    def validate(self) -> bool:
            """
            Validate the current value and set the error message if necessary.

            This method validates the current value of the element based on the defined validation rules.
            If the validation is successful, the error message is set to None.
            If the validation fails, the error message is set to the corresponding error message defined in the validation rules.

            Return:
                - True if the value is valid, False otherwise
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

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        self.validate()
