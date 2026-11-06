import asyncio
from collections.abc import Awaitable, Callable
from typing import Any, Self, TypeAlias, cast

from ... import background_tasks, helpers
from ...events import ValueT
from .value_element import ValueElement

ValidationFunction: TypeAlias = Callable[[ValueT], str | Awaitable[str | None] | None]
ValidationDict: TypeAlias = dict[str, Callable[[ValueT], bool | Awaitable[bool]]]

_ASYNC_RESULT_ERROR = 'The validate method cannot return results for async validation functions.'


def _is_async_validation(validation: ValidationFunction[Any] | ValidationDict[Any] | None) -> bool:
    """Return whether the validation contains an async function."""
    if isinstance(validation, dict):
        return any(helpers.is_coroutine_function(check) for check in validation.values())
    return helpers.is_coroutine_function(validation)


def _discard_awaitable(result: Any) -> None:
    """Close a coroutine that will not be awaited to avoid a "never awaited" warning."""
    if asyncio.iscoroutine(result):
        result.close()


class ValidationElement(ValueElement[ValueT]):

    def __init__(self, validation: ValidationFunction[ValueT] | ValidationDict[ValueT] | None, **kwargs: Any) -> None:
        self._validation = validation
        self._auto_validation = True
        self._error: str | None = None
        self._validation_counter = 0
        super().__init__(**kwargs)
        with self._props.suspend_updates():
            self._props['error'] = None if validation is None else False  # reserve bottom space for error message

    @property
    def validation(self) -> ValidationFunction[ValueT] | ValidationDict[ValueT] | None:
        """The validation function or dictionary of validation functions."""
        return self._validation

    @validation.setter
    def validation(self, validation: ValidationFunction[ValueT] | ValidationDict[ValueT] | None) -> None:
        """Sets the validation function or dictionary of validation functions.

        :param validation: validation function or dictionary of validation functions (``None`` to disable validation)
        """
        self._validation = validation
        self.validate(return_result=False)

    @property
    def error(self) -> str | None:
        """The latest error message from the validation functions."""
        return self._error

    @error.setter
    def error(self, error: str | None) -> None:
        """Sets the error message.

        :param error: The optional error message
        """
        new_error_prop = None if error is None and self.validation is None else (error is not None)
        if self._error == error and self._props.get('error') == new_error_prop:
            return
        self._error = error
        self._props['error'] = new_error_prop
        self._props['error-message'] = error

    def validate(self, *, return_result: bool = True) -> bool:
        """Validate the current value and set the error message if necessary.

        For async validation functions, ``return_result`` must be set to ``False`` and the return value will be ``True``,
        independently of the validation result which is evaluated in the background.

        *Updated in version 2.7.0: Added support for async validation functions.*

        :param return_result: whether to return the result of the validation (default: ``True``)
        :return: whether the validation was successful (always ``True`` for async validation functions)
        """
        if return_result and _is_async_validation(self._validation):
            raise NotImplementedError(_ASYNC_RESULT_ERROR)

        self._validation_counter += 1
        validation_counter = self._validation_counter

        if callable(self._validation):
            result = self._validation(self.value)
            if helpers.should_await(result):
                if return_result:
                    _discard_awaitable(result)
                    raise NotImplementedError(_ASYNC_RESULT_ERROR)

                async def await_error():
                    error = await result
                    if validation_counter == self._validation_counter:
                        self.error = error
                background_tasks.create(await_error(), name=f'validate {self.id}', context=self)
                return True
            self.error = cast(str | None, result)
            return self.error is None

        if isinstance(self._validation, dict):
            value = self.value
            checks = list(self._validation.items())
            for index, (message, check) in enumerate(checks):
                check_result = check(value)
                if helpers.should_await(check_result):
                    if return_result:
                        _discard_awaitable(check_result)
                        raise NotImplementedError(_ASYNC_RESULT_ERROR)

                    async def await_remaining_checks(start: int = index,
                                                     first_check_result: Any = check_result) -> None:
                        error = None
                        for offset, (message, check) in enumerate(checks[start:]):
                            passed = first_check_result if offset == 0 else check(value)
                            if helpers.should_await(passed):
                                passed = await passed
                            if not passed:
                                error = message
                                break
                        if validation_counter == self._validation_counter:
                            self.error = error

                    background_tasks.create(await_remaining_checks(), name=f'validate {self.id}', context=self)
                    return True
                if not check_result:
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
            self.validate(return_result=False)
