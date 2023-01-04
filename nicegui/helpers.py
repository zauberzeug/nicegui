import asyncio
import functools
from contextlib import nullcontext
from typing import Any, Awaitable, Callable, Optional, Union

from . import globals
from .client import Client
from .task_logger import create_task


def is_coroutine(object: Any) -> bool:
    while isinstance(object, functools.partial):
        object = object.func
    return asyncio.iscoroutinefunction(object)


def safe_invoke(func: Union[Callable, Awaitable], client: Optional[Client] = None) -> None:
    try:
        if isinstance(func, Awaitable):
            async def func_with_client():
                with client or nullcontext():
                    await func
            create_task(func_with_client())
        else:
            with client or nullcontext():
                result = func()
            if isinstance(result, Awaitable):
                async def result_with_client():
                    with client or nullcontext():
                        await result
                create_task(result_with_client())
    except:
        globals.log.exception(f'could not invoke {func}')
