import functools
import sys
from collections.abc import Callable
from inspect import Parameter, signature
from typing import Any

if sys.version_info < (3, 13):
    from asyncio import iscoroutinefunction
else:
    from inspect import iscoroutinefunction


def is_coroutine_function(obj: Any) -> bool:
    """Check if the object is a coroutine function.

    This function is needed because functools.partial is not a coroutine function, but its func attribute is.
    Note: It will return false for coroutine objects.
    """
    while isinstance(obj, functools.partial):
        obj = obj.func
    return iscoroutinefunction(obj)


def expects_arguments(func: Callable) -> bool:
    """Check if the function expects non-variable arguments without a default value."""
    return any(p.default is Parameter.empty and
               p.kind is not Parameter.VAR_POSITIONAL and
               p.kind is not Parameter.VAR_KEYWORD
               for p in signature(func).parameters.values())
