import asyncio
import inspect
import time
from typing import Callable

from fastapi import Response

from . import globals
from .client import Client
from .task_logger import create_task


class page:

    def __init__(self, path: str, response_timeout: float = 3.0) -> None:
        self.path = path
        self.response_timeout = response_timeout
        # NOTE we need to remove existing routes for this path to make sure only the latest definition is used
        globals.app.routes[:] = [r for r in globals.app.routes if r.path != path]

    def __call__(self, func: Callable) -> Callable:
        async def decorated(*dec_args, **dec_kwargs) -> Response:
            try:
                with Client() as client:
                    if any(p.name == 'client' for p in inspect.signature(func).parameters.values()):
                        dec_kwargs['client'] = client
                    result = func(*dec_args, **dec_kwargs)
                if inspect.isawaitable(result):
                    async def wait_for_result() -> Response:
                        with client:
                            await result
                    task = create_task(wait_for_result())
                    deadline = time.time() + self.response_timeout
                    while task and not client.is_waiting_for_handshake and not task.done():
                        if time.time() > deadline:
                            raise TimeoutError(f'Response not ready after {self.response_timeout} seconds')
                        await asyncio.sleep(0.1)
                    result = task.result() if task.done() else None
                if isinstance(result, Response):  # NOTE if setup returns a response, we don't need to render the page
                    return result
                return client.build_response()
            except Exception as e:
                globals.log.exception(e)

        parameters = [p for p in inspect.signature(func).parameters.values() if p.name != 'client']
        decorated.__signature__ = inspect.Signature(parameters)

        return globals.app.get(self.path)(decorated)
