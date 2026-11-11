import asyncio
from collections.abc import Awaitable, Callable, Iterator, Mapping
from typing import Any, Self, TypeAlias, cast

from ... import background_tasks, helpers
from ...events import ValueT
from .value_element import ValueElement

ValidationFunction: TypeAlias = Callable[[ValueT], str | Awaitable[str | None] | None]
ValidationDict: TypeAlias = Mapping[str, Callable[[ValueT], bool | Awaitable[bool]]]


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

        For async validation functions, also inside a validation dictionary,
        ``return_result`` must be set to ``False`` and the return value will be ``True``,
        independently of the validation result which is evaluated in the background.

        *Updated in version 2.7.0: Added support for async validation functions.*

        *Updated in version 4.1.0: Added support for async functions in validation dictionaries.*

        :param return_result: whether to return the result of the validation (default: ``True``)
        :return: whether the validation was successful (always ``True`` for async validation functions)
        """
        result = self._run_validation(return_result)
        self._validation_counter += 1
        validation_counter = self._validation_counter
        if helpers.should_await(result):
            async def await_error():
                error = await result
                if validation_counter == self._validation_counter:
                    self.error = error
            background_tasks.create(await_error(), name=f'validate {self.id}', context=self)
            return True
        self.error = cast(str | None, result)
        return self.error is None

    def _run_validation(self, return_result: bool) -> str | Awaitable[str | None] | None:
        """Run the validation function or the checks of the validation dictionary and return the (awaitable) error."""
        value = self.value
        if callable(self._validation):
            result = self._validation(value)
            if return_result:
                _reject_awaitable(result)
            return result
        if isinstance(self._validation, Mapping):
            checks = iter(self._validation.items())
            for message, check in checks:
                passed = check(value)
                if helpers.should_await(passed):
                    if return_result:
                        _reject_awaitable(passed)
                    return _await_remaining_checks(passed, message, checks, value)
                if not passed:
                    return message
        return None

    def without_auto_validation(self) -> Self:
        """Disable automatic validation on value change."""
        self._auto_validation = False
        return self

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if self._auto_validation:
            self.validate(return_result=False)


def _reject_awaitable(result: Any) -> None:
    """Raise if the result is an awaitable, closing a coroutine first to avoid a "never awaited" warning."""
    if helpers.should_await(result):
        if asyncio.iscoroutine(result):
            result.close()
        raise NotImplementedError('The validate method cannot return results for async validation functions.')


async def _await_remaining_checks(pending: Awaitable[bool],
                                  pending_message: str,
                                  checks: Iterator[tuple[str, Callable[[Any], bool | Awaitable[bool]]]],
                                  value: Any) -> str | None:
    """Await the pending check and run the remaining checks one by one, returning the first failing message."""
    if not await pending:
        return pending_message
    for message, check in checks:
        result = check(value)
        if helpers.should_await(result):
            result = await result
        if not result:
            return message
    return None
