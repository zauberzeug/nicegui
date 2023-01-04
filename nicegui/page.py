import asyncio
import inspect
import time
from typing import Callable, Optional

from fastapi import Request, Response

from . import globals
from .async_updater import AsyncUpdater
from .client import Client
from .favicon import create_favicon_route
from .task_logger import create_task


class page:

    def __init__(self,
                 path: str, *,
                 title: Optional[str] = None,
                 favicon: Optional[str] = None,
                 dark: Optional[bool] = ...,
                 response_timeout: float = 3.0,
                 ) -> None:
        """Page

        Creates a new page at the given route.

        :param path: route of the new page (path must start with '/')
        :param title: optional page title
        :param favicon: optional relative filepath or absolute URL to a favicon (default: `None`, NiceGUI icon will be used)
        :param dark: whether to use Quasar's dark mode (defaults to `dark` argument of `run` command)
        :param response_timeout: maximum time for the decorated function to build the page (default: 3.0)
        """
        self.path = path
        self.title = title
        self.favicon = favicon
        self.dark = dark
        self.response_timeout = response_timeout

        create_favicon_route(self.path, favicon)

    def resolve_title(self) -> str:
        return self.title if self.title is not None else globals.title

    def resolve_dark(self) -> Optional[bool]:
        return self.dark if self.dark is not ... else globals.dark

    def __call__(self, func: Callable) -> Callable:
        # NOTE we need to remove existing routes for this path to make sure only the latest definition is used
        globals.app.routes[:] = [r for r in globals.app.routes if getattr(r, 'path', None) != self.path]
        parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

        async def decorated(*dec_args, **dec_kwargs) -> Response:
            request = dec_kwargs['request']
            # NOTE cleaning up the keyword args so the signature is consistent with "func" again
            dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
            with Client(self) as client:
                if any(p.name == 'client' for p in inspect.signature(func).parameters.values()):
                    dec_kwargs['client'] = client
                result = func(*dec_args, **dec_kwargs)
            if inspect.isawaitable(result):
                async def wait_for_result() -> None:
                    with client:
                        await AsyncUpdater(result)
                task = create_task(wait_for_result())
                deadline = time.time() + self.response_timeout
                while task and not client.is_waiting_for_handshake and not task.done():
                    if time.time() > deadline:
                        raise TimeoutError(f'Response not ready after {self.response_timeout} seconds')
                    await asyncio.sleep(0.1)
                result = task.result() if task.done() else None
            if isinstance(result, Response):  # NOTE if setup returns a response, we don't need to render the page
                return result
            return client.build_response(request)

        parameters = [p for p in inspect.signature(func).parameters.values() if p.name != 'client']
        # NOTE adding request as a parameter so we can pass it to the client in the decorated function
        if 'request' not in [p.name for p in parameters]:
            parameters.append(inspect.Parameter('request', inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Request))
        decorated.__signature__ = inspect.Signature(parameters)

        globals.page_routes[decorated] = self.path

        return globals.app.get(self.path)(decorated)
