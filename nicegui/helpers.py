import asyncio
import functools
import inspect
from contextlib import nullcontext
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Union

from . import background_tasks, globals

if TYPE_CHECKING:
    from .client import Client


def is_coroutine(object: Any) -> bool:
    while isinstance(object, functools.partial):
        object = object.func
    return asyncio.iscoroutinefunction(object)


def safe_invoke(func: Union[Callable, Awaitable], client: Optional['Client'] = None) -> None:
    try:
        if isinstance(func, Awaitable):
            async def func_with_client():
                with client or nullcontext():
                    await func
            background_tasks.create(func_with_client())
        else:
            with client or nullcontext():
                result = func(client) if len(inspect.signature(func).parameters) == 1 and client is not None else func()
            if isinstance(result, Awaitable):
                async def result_with_client():
                    with client or nullcontext():
                        await result
                background_tasks.create(result_with_client())
    except Exception as e:
        globals.handle_exception(e)
