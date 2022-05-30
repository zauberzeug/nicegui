import asyncio
import inspect
import time
import uuid
from typing import Callable, Optional

import justpy as jp
from pygments.formatters import HtmlFormatter
from starlette.requests import Request

from ..globals import config, page_stack, view_stack
from ..helpers import is_coroutine


class Page(jp.QuasarPage):

    def __init__(self,
                 route: str,
                 title: Optional[str] = None,
                 favicon: Optional[str] = None,
                 dark: Optional[bool] = ...,
                 classes: str = 'q-ma-md column items-start',
                 css: str = HtmlFormatter().get_style_defs('.codehilite'),
                 on_connect: Optional[Callable] = None,
                 ):
        """Page

        Creates a new page at the given path.

        :param route: route of the new page (path must start with '/')
        :param title: optional page title
        :param favicon: optional favicon
        :param dark: whether to use Quasar's dark mode (defaults to `dark` argument of `run` command)
        :param classes: tailwind classes for the container div (default: `'q-ma-md column items-start'`)
        :param css: CSS definitions
        :param on_connect: optional function or coroutine which is called for each new client connection
        """
        super().__init__()

        self.delete_flag = False
        self.title = title or config.title
        self.favicon = favicon or config.favicon
        self.dark = dark if dark is not ... else config.dark
        self.tailwind = True  # use Tailwind classes instead of Quasars
        self.css = css
        self.on_connect = on_connect or config.on_connect

        self.waiting_javascript_commands: dict[str, str] = {}
        self.on('result_ready', self.handle_javascript_result)

        self.view = jp.Div(a=self, classes=classes, style='row-gap: 1em', temp=False)
        self.view.add_page(self)

        self.route = route
        jp.Route(route, self._route_function)

    async def _route_function(self, request: Request):
        if self.on_connect:
            arg_count = len(inspect.signature(self.on_connect).parameters)
            is_coro = is_coroutine(self.on_connect)
            if arg_count == 1:
                await self.on_connect(request) if is_coro else self.on_connect(request)
            elif arg_count == 0:
                await self.on_connect() if is_coro else self.on_connect()
            else:
                raise ValueError(f'invalid number of arguments (0 or 1 allowed, got {arg_count})')
        return self

    def __enter__(self):
        page_stack.append(self)
        view_stack.append(self.view)
        return self

    def __exit__(self, *_):
        page_stack.pop()
        view_stack.pop()

    async def await_javascript(self, code: str, check_interval: float = 0.01, timeout: float = 1.0) -> str:
        start_time = time.time()
        request_id = str(uuid.uuid4())
        await self.run_javascript(code, request_id=request_id)
        while request_id not in self.waiting_javascript_commands:
            if time.time() > start_time + timeout:
                raise TimeoutError('JavaScript did not respond in time')
            await asyncio.sleep(check_interval)
        return self.waiting_javascript_commands.pop(request_id)

    def handle_javascript_result(self, msg):
        self.waiting_javascript_commands[msg.request_id] = msg.result
