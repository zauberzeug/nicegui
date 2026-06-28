import asyncio
import functools
import sys
import weakref
from collections.abc import Awaitable, Callable
from contextlib import AbstractContextManager
from inspect import Parameter, signature
from types import FunctionType, MethodType
from typing import Any, TypeGuard, TypeVar

from ..awaitable_response import AwaitableResponse
from .warnings import warn_once

if sys.version_info < (3, 13):
    from asyncio import iscoroutinefunction
else:
    from inspect import iscoroutinefunction

_T = TypeVar('_T')


class _CallableCache:
    """Cache by callable identity without keeping user callables alive."""

    def __init__(self) -> None:
        self._cache: dict[int, tuple[weakref.ref[Any], bool]] = {}

    def get(self, func: Callable) -> bool | None:
        func_id = id(func)
        entry = self._cache.get(func_id)
        if entry is None:
            return None
        ref, result = entry
        if ref() is func:
            return result
        self._cache.pop(func_id, None)
        return None

    def set(self, func: Callable, result: bool) -> None:
        func_id = id(func)
        try:
            def remove(_: weakref.ReferenceType[Any], func_id: int = func_id) -> None:
                self._cache.pop(func_id, None)

            ref = weakref.ref(func, remove)
        except TypeError:
            return
        self._cache[func_id] = (ref, result)


_expects_arguments_cache = _CallableCache()


def _expects_arguments_from_python_callable(func: Callable) -> bool | None:
    """Fast path for ordinary Python functions and bound methods.

    Return ``None`` when a callable may have a custom signature and needs ``inspect.signature``.
    """
    if isinstance(func, MethodType):
        function = func.__func__
        bound_positional_count = 1
    elif isinstance(func, FunctionType):
        function = func
        bound_positional_count = 0
    else:
        return None
    if hasattr(function, '__signature__') or hasattr(function, '__wrapped__'):
        return None

    code = function.__code__
    required_positional = code.co_argcount - len(function.__defaults__ or ()) - bound_positional_count
    if required_positional > 0:
        return True
    if code.co_kwonlyargcount:
        keyword_only_names = code.co_varnames[code.co_argcount:code.co_argcount + code.co_kwonlyargcount]
        keyword_defaults = function.__kwdefaults__ or {}
        return any(name not in keyword_defaults for name in keyword_only_names)
    return False


def is_coroutine_function(obj: Any) -> bool:
    """Check if the object is a coroutine function.

    This function is needed because functools.partial is not a coroutine function, but its func attribute is.
    Note: It will return false for coroutine objects.
    """
    while isinstance(obj, functools.partial):
        obj = obj.func
    return iscoroutinefunction(obj)


def _expects_arguments_from_signature(func: Callable) -> bool:
    return any(p.default is Parameter.empty and
               p.kind is not Parameter.VAR_POSITIONAL and
               p.kind is not Parameter.VAR_KEYWORD
               for p in signature(func).parameters.values())


def expects_arguments(func: Callable) -> bool:
    """Check if the function expects non-variable arguments without a default value."""
    fast_result = _expects_arguments_from_python_callable(func)
    if fast_result is not None:
        return fast_result
    cached_result = _expects_arguments_cache.get(func)
    if cached_result is not None:
        return cached_result
    result = _expects_arguments_from_signature(func)
    _expects_arguments_cache.set(func, result)
    return result


class NoImplicitAwait:
    """Marker base for awaitables that must not be implicitly awaited by event handlers."""


def should_await(result: Any) -> TypeGuard[Awaitable[Any]]:
    """Determine if a result should be awaited.

    Returns ``True`` for awaitables that are not already managed
    (i.e. not an ``AwaitableResponse`` or an ``asyncio.Task``).

    Note: We want to await an awaitable result even if the handler is not an async function (like a lambda statement).

    Subclasses of ``NoImplicitAwait`` are also excluded
    so that chainable mutators returning ``self`` on awaitable elements (like ``Dialog``) are not silently awaited.
    """
    if result is None or not hasattr(result, '__await__'):
        return False
    return isinstance(result, Awaitable) and not isinstance(result, (NoImplicitAwait, AwaitableResponse, asyncio.Task))


async def await_with_context(awaitable: Awaitable[_T], context: AbstractContextManager) -> _T:
    """Await an awaitable within a context manager."""
    with context:
        return await awaitable


def normalize_lifecycle_handler(handler: Callable[..., Any] | Awaitable[Any], registration: str) -> Callable[..., Any]:
    """Normalize lifecycle handler registration for callable-only and deprecated-awaitable paths."""
    if callable(handler):
        return handler
    if not isinstance(handler, Awaitable):
        raise TypeError(f'{registration} expects a synchronous or asynchronous function.')

    # DEPRECATED: remove direct awaitable lifecycle registrations in NiceGUI 4.0
    def wrapped_handler() -> Awaitable[Any]:
        return handler
    warn_once(f'Passing an awaitable directly to {registration} is deprecated and will be removed in NiceGUI 4.0. '
              'Pass a synchronous or asynchronous function instead.')
    wrapped_handler.__name__ = f'deprecated {registration} awaitable'
    return wrapped_handler
