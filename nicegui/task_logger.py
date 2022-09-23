'''original copied from https://quantlane.com/blog/ensure-asyncio-task-exceptions-get-logged/'''

import asyncio
import functools
import logging
import sys
from typing import Any, Awaitable, Optional, Tuple, TypeVar

from . import globals

T = TypeVar('T')


def create_task(
    coroutine: Awaitable[T],
    *,
    loop: Optional[asyncio.AbstractEventLoop] = None,
    name: str = 'unnamed task',
) -> 'asyncio.Task[T]':  # This type annotation has to be quoted for Python < 3.9, see https://www.python.org/dev/peps/pep-0585/
    '''
    This helper function wraps a ``loop.create_task(coroutine())`` call and ensures there is
    an exception handler added to the resulting task. If the task raises an exception it is logged
    using the provided ``logger``, with additional context provided by ``message`` and optionally
    ``message_args``.
    '''

    logger = logging.getLogger(__name__)
    message = 'Task raised an exception'
    message_args = ()
    if loop is None:
        loop = globals.loop
    if sys.version_info[1] < 8:
        task = loop.create_task(coroutine)  # name parameter is only supported from 3.8 onward
    else:
        task = loop.create_task(coroutine, name=name)
    task.add_done_callback(
        functools.partial(_handle_task_result, logger=logger, message=message, message_args=message_args)
    )
    return task


def _handle_task_result(
    task: asyncio.Task,
    *,
    logger: logging.Logger,
    message: str,
    message_args: Tuple[Any, ...] = (),
) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass  # Task cancellation should not be logged as an error.
    # Ad the pylint ignore: we want to handle all exceptions here so that the result of the task
    # is properly logged. There is no point re-raising the exception in this callback.
    except Exception:  # pylint: disable=broad-except
        logger.exception(message, *message_args)
