import asyncio
import functools
from typing import Any, Awaitable, Callable, Union

from . import globals
from .task_logger import create_task


def is_coroutine(object: Any) -> bool:
    while isinstance(object, functools.partial):
        object = object.func
    return asyncio.iscoroutinefunction(object)


def safe_invoke(func: Union[Callable, Awaitable]) -> None:
    try:
        if isinstance(func, Awaitable):
            create_task(func)
        else:
            result = func()
            if isinstance(result, Awaitable):
                create_task(result)
    except:
        globals.log.exception(f'could not invoke {func}')
