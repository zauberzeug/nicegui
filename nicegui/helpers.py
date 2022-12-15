import asyncio
import functools
import inspect
import time
from typing import Any, Awaitable, Callable, Union

from . import globals
from .task_logger import create_task


def measure(*, reset: bool = False, ms: bool = False) -> None:
    global t
    if 't' in globals() and not reset:
        dt = time.time() - t
        line = inspect.stack()[1][0].f_lineno
        output = f'{dt * 1000:7.3f} ms' if ms else f'{dt:7.3f} s'
        print(f'{inspect.stack()[1].filename}:{line}', output, flush=True)
    if reset:
        print('------------', flush=True)
    t = time.time()


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
