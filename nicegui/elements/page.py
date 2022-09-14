import asyncio
import inspect
import time
import uuid
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Optional

import justpy as jp
from addict import Dict
from pygments.formatters import HtmlFormatter
from starlette.requests import Request

from ..globals import config, connect_handlers, disconnect_handlers, page_builders, view_stack
from ..helpers import is_coroutine


@dataclass
class PageBuilder:
    function: Callable
    shared: bool


class Page(jp.QuasarPage):

    def __init__(self,
                 route: str,
                 title: Optional[str] = None,
                 *,
                 favicon: Optional[str] = None,
                 dark: Optional[bool] = ...,
                 classes: str = 'q-ma-md column items-start',
                 css: str = HtmlFormatter().get_style_defs('.codehilite'),
                 on_connect: Optional[Callable] = None,
                 on_page_ready: Optional[Callable] = None,
                 on_disconnect: Optional[Callable] = None,
                 shared: bool = False,
                 ):
        super().__init__()

        self.route = route
        self.title = title or config.title
        self.favicon = favicon or config.favicon
        self.dark = dark if dark is not ... else config.dark
        self.tailwind = True  # use Tailwind classes instead of Quasars
        self.css = css
        self.connect_handler = on_connect
        self.page_ready_handler = on_page_ready
        self.disconnect_handler = on_disconnect
        self.delete_flag = not shared

        self.waiting_javascript_commands: dict[str, str] = {}
        self.on('result_ready', self.handle_javascript_result)
        self.on('page_ready', self.handle_page_ready)

        self.view = jp.Div(a=self, classes=classes, style='row-gap: 1em', temp=False)
        self.view.add_page(self)

    async def _route_function(self, request: Request):
        for connect_handler in connect_handlers + ([self.connect_handler] if self.connect_handler else []):
            arg_count = len(inspect.signature(connect_handler).parameters)
            is_coro = is_coroutine(connect_handler)
            if arg_count == 1:
                await connect_handler(request) if is_coro else connect_handler(request)
            elif arg_count == 0:
                await connect_handler() if is_coro else connect_handler()
            else:
                raise ValueError(f'invalid number of arguments (0 or 1 allowed, got {arg_count})')
        return self

    async def handle_page_ready(self, msg: Dict) -> bool:
        if self.page_ready_handler:
            arg_count = len(inspect.signature(self.page_ready_handler).parameters)
            is_coro = is_coroutine(self.page_ready_handler)
            if arg_count == 1:
                await self.page_ready_handler(msg.websocket) if is_coro else self.page_ready_handler(msg.websocket)
            elif arg_count == 0:
                await self.page_ready_handler() if is_coro else self.page_ready_handler()
            else:
                raise ValueError(f'invalid number of arguments (0 or 1 allowed, got {arg_count})')
        return False

    async def on_disconnect(self, websocket=None) -> None:
        for disconnect_handler in ([self.disconnect_handler] if self.disconnect_handler else []) + disconnect_handlers:
            arg_count = len(inspect.signature(disconnect_handler).parameters)
            is_coro = is_coroutine(disconnect_handler)
            if arg_count == 1:
                await disconnect_handler(websocket) if is_coro else disconnect_handler(websocket)
            elif arg_count == 0:
                await disconnect_handler() if is_coro else disconnect_handler()
            else:
                raise ValueError(f'invalid number of arguments (0 or 1 allowed, got {arg_count})')
        await super().on_disconnect(websocket)

    async def await_javascript(self, code: str, check_interval: float = 0.01, timeout: float = 1.0) -> str:
        start_time = time.time()
        request_id = str(uuid.uuid4())
        await self.run_javascript(code, request_id=request_id)
        while request_id not in self.waiting_javascript_commands:
            if time.time() > start_time + timeout:
                raise TimeoutError('JavaScript did not respond in time')
            await asyncio.sleep(check_interval)
        return self.waiting_javascript_commands.pop(request_id)

    def handle_javascript_result(self, msg) -> bool:
        self.waiting_javascript_commands[msg.request_id] = msg.result
        return False


def add_head_html(self, html: str) -> None:
    for page in get_current_view().pages.values():
        page.head_html += html


def add_body_html(self, html: str) -> None:
    for page in get_current_view().pages.values():
        page.body_html += html


def page(self,
         route: str,
         title: Optional[str] = None,
         *,
         favicon: Optional[str] = None,
         dark: Optional[bool] = ...,
         classes: str = 'q-ma-md column items-start',
         css: str = HtmlFormatter().get_style_defs('.codehilite'),
         on_connect: Optional[Callable] = None,
         on_page_ready: Optional[Callable] = None,
         on_disconnect: Optional[Callable] = None,
         shared: bool = False,
         ):
    """Page

    Creates a new page at the given route.

    :param route: route of the new page (path must start with '/')
    :param title: optional page title
    :param favicon: optional favicon
    :param dark: whether to use Quasar's dark mode (defaults to `dark` argument of `run` command)
    :param classes: tailwind classes for the container div (default: `'q-ma-md column items-start'`)
    :param css: CSS definitions
    :param on_connect: optional function or coroutine which is called for each new client connection
    :param on_page_ready: optional function or coroutine which is called when the websocket is connected
    :param on_disconnect: optional function or coroutine which is called when a client disconnects
    :param shared: whether the page instance is shared between multiple clients (default: `False`)
    """
    def decorator(func):
        @wraps(func)
        async def decorated():
            page = Page(
                route=route,
                title=title,
                favicon=favicon,
                dark=dark,
                classes=classes,
                css=css,
                on_connect=on_connect,
                on_page_ready=on_page_ready,
                on_disconnect=on_disconnect,
                shared=shared,
            )
            view_stack.append(page.view)
            await func() if is_coroutine(func) else func()
            view_stack.pop()
            return page
        page_builders[route] = PageBuilder(decorated, shared)
        return decorated
    return decorator


def get_current_view() -> jp.HTMLBaseComponent:
    if not view_stack:
        page = Page('/')
        page.delete_flag = False
        view_stack.append(page.view)
        jp.Route('/', page._route_function)
    return view_stack[-1]
