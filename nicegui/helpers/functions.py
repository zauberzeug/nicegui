import asyncio
from collections.abc import Awaitable, Callable
from contextlib import AbstractContextManager
from inspect import Parameter, signature
from typing import Any, TypeGuard, TypeVar

from ..awaitable_response import AwaitableResponse
from .warnings import warn_once

_T = TypeVar('_T')


def expects_arguments(func: Callable) -> bool:
    """Check if the function expects non-variable arguments without a default value."""
    return any(p.default is Parameter.empty and
               p.kind is not Parameter.VAR_POSITIONAL and
               p.kind is not Parameter.VAR_KEYWORD
               for p in signature(func).parameters.values())


def should_await(result: Any) -> TypeGuard[Awaitable[Any]]:
    """Determine if a result should be awaited.

    Returns ``True`` for awaitables that are not already managed
    (i.e. not an ``AwaitableResponse`` or an ``asyncio.Task``).

    Note: We want to await an awaitable result even if the handler is not an async function (like a lambda statement).
    """
    return isinstance(result, Awaitable) and not isinstance(result, (AwaitableResponse, asyncio.Task))


async def await_with_context(awaitable: Awaitable[_T], ctx: AbstractContextManager) -> _T:
    """Await an awaitable within a context manager."""
    with ctx:
        return await awaitable


def normalize_lifecycle_handler(
    handler: Callable[..., Any] | Awaitable[Any],
    registration: str, *,
    reject: bool = True,
) -> Callable[..., Any]:
    """Normalize lifecycle handler registration for callable-only and deprecated-awaitable paths."""
    if callable(handler):
        return handler
    if not isinstance(handler, Awaitable):
        raise TypeError(f'{registration} expects a synchronous or asynchronous function.')

    if reject:
        raise TypeError(f'{registration} expects a synchronous or asynchronous function, not an awaitable object. '
                        'Pass the function itself instead of calling it.',)

    # DEPRECATED: remove direct awaitable lifecycle registrations in NiceGUI 4.0
    def wrapped_handler() -> Awaitable[Any]:
        return handler
    warn_once(f'Passing an awaitable directly to {registration} is deprecated and will be removed in NiceGUI 4.0. '
              'Pass a synchronous or asynchronous function instead.')
    wrapped_handler.__name__ = f'deprecated {registration} awaitable'
    return wrapped_handler
