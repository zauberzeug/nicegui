from __future__ import annotations

import asyncio
import inspect
import time
import types
import uuid
from functools import wraps
from typing import Callable, Dict, Generator, List, Optional

import justpy as jp
from addict import Dict as AdDict
from pygments.formatters import HtmlFormatter
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.routing import Route, compile_path
from starlette.websockets import WebSocket

from . import globals
from .auto_context import Context, get_view_stack
from .events import PageEvent
from .helpers import is_coroutine
from .page_builder import PageBuilder
from .routes import add_route, convert_arguments


class Page(jp.QuasarPage):

    def __init__(self,
                 title: Optional[str] = None,
                 *,
                 favicon: Optional[str] = None,
                 dark: Optional[bool] = ...,
                 classes: str = 'q-pa-md column items-start gap-4',
                 css: str = HtmlFormatter().get_style_defs('.codehilite'),
                 on_connect: Optional[Callable] = None,
                 on_page_ready: Optional[Callable] = None,
                 on_disconnect: Optional[Callable] = None,
                 shared: bool = False,
                 ) -> None:
        super().__init__()

        if globals.config:
            self.title = title or globals.config.title
            self.set_favicon(favicon or globals.config.favicon)
            self.dark = dark if dark is not ... else globals.config.dark
        else:
            self.title = title
            self.set_favicon(favicon)
            self.dark = dark if dark is not ... else None
        self.tailwind = True  # use Tailwind classes instead of Quasars
        self.css = css
        self.connect_handler = on_connect
        self.page_ready_handler = on_page_ready
        self.page_ready_generator: Optional[Generator[None, PageEvent, None]] = None
        self.disconnect_handler = on_disconnect
        self.shared = shared
        self.delete_flag = not shared

        self.waiting_javascript_commands: Dict[str, str] = {}
        self.on('result_ready', self.handle_javascript_result)
        self.on('page_ready', self.handle_page_ready)

        self.layout = jp.QLayout(a=self, view='HHH LpR FFF', temp=False)
        container = jp.QPageContainer(a=self.layout, temp=False)
        self.view = jp.Div(a=container, classes=classes, temp=False)
        self.view.add_page(self)

    def set_favicon(self, favicon: Optional[str]) -> None:
        if not favicon:
            self.favicon = 'favicon.ico'
        elif favicon.startswith('http://') or favicon.startswith('https://'):
            self.favicon = favicon
        else:
            self.favicon = f'_favicon/{favicon}'

    async def _route_function(self, request: Request) -> Page:
        with Context(self.view):
            for handler in globals.connect_handlers + ([self.connect_handler] if self.connect_handler else []):
                arg_count = len(inspect.signature(handler).parameters)
                is_coro = is_coroutine(handler)
                if arg_count == 1:
                    await handler(request) if is_coro else handler(request)
                elif arg_count == 0:
                    await handler() if is_coro else handler()
                else:
                    raise ValueError(f'invalid number of arguments (0 or 1 allowed, got {arg_count})')
        return self

    async def handle_page_ready(self, msg: AdDict) -> bool:
        with Context(self.view) as context:
            try:
                if self.page_ready_generator is not None:
                    if isinstance(self.page_ready_generator, types.AsyncGeneratorType):
                        await context.watch_asyncs(self.page_ready_generator.asend(PageEvent(msg.websocket)))
                    elif isinstance(self.page_ready_generator, types.GeneratorType):
                        self.page_ready_generator.send(PageEvent(msg.websocket))
            except (StopIteration, StopAsyncIteration):
                pass  # after the page_ready_generator returns, it will raise StopIteration; it's part of the generator protocol and expected
            except:
                globals.log.exception('Failed to execute page-ready')
            try:
                if self.page_ready_handler:
                    arg_count = len(inspect.signature(self.page_ready_handler).parameters)
                    is_coro = is_coroutine(self.page_ready_handler)
                    if arg_count == 1:
                        result = self.page_ready_handler(msg.websocket)
                    elif arg_count == 0:
                        result = self.page_ready_handler()
                    else:
                        raise ValueError(f'invalid number of arguments (0 or 1 allowed, got {arg_count})')
                    if is_coro:
                        await context.watch_asyncs(result)
            except:
                globals.log.exception('Failed to execute page-ready')
        return False

    async def on_disconnect(self, websocket: Optional[WebSocket] = None) -> None:
        with Context(self.view):
            for handler in globals.disconnect_handlers + ([self.disconnect_handler] if self.disconnect_handler else[]):
                arg_count = len(inspect.signature(handler).parameters)
                is_coro = is_coroutine(handler)
                if arg_count == 1:
                    await handler(websocket) if is_coro else handler(websocket)
                elif arg_count == 0:
                    await handler() if is_coro else handler()
                else:
                    raise ValueError(f'invalid number of arguments (0 or 1 allowed, got {arg_count})')
        await super().on_disconnect(websocket)

    async def run_javascript_on_socket(self, code: str, websocket: WebSocket, *,
                                       respond: bool = True, timeout: float = 1.0, check_interval: float = 0.01) -> Optional[str]:
        start_time = time.time()
        request_id = str(uuid.uuid4())
        await websocket.send_json({'type': 'run_javascript', 'data': code, 'request_id': request_id, 'send': respond})
        if not respond:
            return
        while request_id not in self.waiting_javascript_commands:
            if time.time() > start_time + timeout:
                raise TimeoutError('JavaScript did not respond in time')
            await asyncio.sleep(check_interval)
        return self.waiting_javascript_commands.pop(request_id)

    async def run_javascript(self, code: str, *,
                             respond: bool = True, timeout: float = 1.0, check_interval: float = 0.01) -> Dict[WebSocket, Optional[str]]:
        if self.page_id not in jp.WebPage.sockets:
            raise RuntimeError('Cannot run JavaScript, because page is not ready.')
        sockets = list(jp.WebPage.sockets[self.page_id].values())
        results = await asyncio.gather(
            *[self.run_javascript_on_socket(code, socket, respond=respond, timeout=timeout, check_interval=check_interval)
              for socket in sockets], return_exceptions=True)
        return dict(zip(sockets, results))

    def handle_javascript_result(self, msg: AdDict) -> bool:
        self.waiting_javascript_commands[msg.request_id] = msg.result
        return False


def add_head_html(self, html: str) -> None:
    find_parent_page().head_html += html


def add_body_html(self, html: str) -> None:
    find_parent_page().body_html += html


async def run_javascript(self, code: str, *,
                         respond: bool = True, timeout: float = 1.0, check_interval: float = 0.01) -> Dict[WebSocket, Optional[str]]:
    return await find_parent_page().run_javascript(code, respond=respond, timeout=timeout, check_interval=check_interval)


class page:
    def __init__(
        self,
        route: str,
        title: Optional[str] = None,
        *,
        favicon: Optional[str] = None,
        dark: Optional[bool] = ...,
        classes: str = 'q-pa-md column items-start gap-4',
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
        :param favicon: optional relative filepath to a favicon (default: `None`, NiceGUI icon will be used)
        :param dark: whether to use Quasar's dark mode (defaults to `dark` argument of `run` command)
        :param classes: tailwind classes for the container div (default: `'q-pa-md column items-start gap-4'`)
        :param css: CSS definitions
        :param on_connect: optional function or coroutine which is called for each new client connection
        :param on_page_ready: optional function or coroutine which is called when the websocket is connected;  see `"Yielding for Page-Ready" <https://nicegui.io/reference#yielding_for_page-ready>`_ as an alternative.
        :param on_disconnect: optional function or coroutine which is called when a client disconnects
        :param shared: whether the page instance is shared between multiple clients (default: `False`)
        """
        self.route = route
        self.title = title
        self.favicon = favicon
        self.dark = dark
        self.classes = classes
        self.css = css
        self.on_connect = on_connect
        self.on_page_ready = on_page_ready
        self.on_disconnect = on_disconnect
        self.shared = shared
        self.page: Optional[Page] = None
        *_, self.converters = compile_path(route)

    def __call__(self, func: Callable, **kwargs) -> Callable:
        @wraps(func)
        async def decorated(request: Optional[Request] = None) -> Page:
            self.page = Page(
                title=self.title,
                favicon=self.favicon,
                dark=self.dark,
                classes=self.classes,
                css=self.css,
                on_connect=self.on_connect,
                on_page_ready=self.on_page_ready,
                on_disconnect=self.on_disconnect,
                shared=self.shared,
            )
            try:
                with Context(self.page.view):
                    if 'request' in inspect.signature(func).parameters:
                        if self.shared:
                            raise RuntimeError('Cannot use `request` argument in shared page')
                    await self.connected(request)
                    await self.before_content()
                    args = {**kwargs, **convert_arguments(request, self.converters, func)}
                    result = await func(**args) if is_coroutine(func) else func(**args)
                    if isinstance(result, types.GeneratorType):
                        if self.shared:
                            raise RuntimeError('Yielding for page_ready is not supported on shared pages')
                        next(result)
                    if isinstance(result, types.AsyncGeneratorType):
                        if self.shared:
                            raise RuntimeError('Yielding for page_ready is not supported on shared pages')
                        await result.__anext__()
                    self.page.page_ready_generator = result
                    await self.after_content()
                return self.page
            except Exception as e:
                globals.log.exception(e)
                return error(500, str(e))
        builder = PageBuilder(decorated, self.shared, self.favicon)
        if globals.state != globals.State.STOPPED:
            builder.create_route(self.route)
        globals.page_builders[self.route] = builder
        return decorated

    async def connected(self, request: Optional[Request]) -> None:
        pass

    async def before_content(self) -> None:
        pass

    async def after_content(self) -> None:
        pass


def find_parent_view() -> jp.HTMLBaseComponent:
    view_stack = get_view_stack()
    if not view_stack:
        if globals.loop and globals.loop.is_running():
            raise RuntimeError('cannot find parent view, view stack is empty')
        page = Page(shared=True)
        view_stack.append(page.view)
        jp.Route('/', page._route_function)
    return view_stack[-1]


def find_parent_page() -> Page:
    pages = list(find_parent_view().pages.values())
    assert len(pages) == 1
    return pages[0]


def error(status_code: int, message: Optional[str] = None) -> Page:
    title = globals.config.title if globals.config else f'Error {status_code}'
    favicon = globals.config.favicon if globals.config else None
    dark = globals.config.dark if globals.config else False
    wp = Page(title=title, favicon=favicon, dark=dark)
    div = jp.Div(a=wp.view, classes='w-full py-20 text-center')
    jp.Div(a=div, classes='text-8xl py-5', text='☹',
           style='font-family: "Arial Unicode MS", "Times New Roman", Times, serif;')
    jp.Div(a=div, classes='text-6xl py-5', text=status_code)
    if 400 <= status_code <= 499:
        title = "This page doesn't exist"
    elif 500 <= status_code <= 599:
        title = 'Server error'
    else:
        title = 'Unknown error'
    if message is not None:
        title += ':'
    jp.Div(a=div, classes='text-xl pt-5', text=title)
    jp.Div(a=div, classes='text-lg pt-2 text-gray-500', text=message or '')
    return wp


def init_auto_index_page() -> None:
    view_stack: List[jp.HTMLBaseComponent] = globals.view_stacks.get(0, [])
    if not view_stack:
        return  # there is no auto-index page on the view stack
    page: Page = view_stack.pop().pages[0]
    page.title = globals.config.title
    page.set_favicon(globals.config.favicon)
    page.dark = globals.config.dark
    page.view.classes = globals.config.main_page_classes
    assert len(view_stack) == 0


def create_page_routes() -> None:
    jp.Route("/{path:path}", lambda: error(404), last=True)
    for route, page_builder in globals.page_builders.items():
        page_builder.create_route(route)


def create_favicon_routes() -> None:
    for page_builder in globals.page_builders.values():
        if page_builder.favicon:
            add_route(None, Route(f'/static/_favicon/{page_builder.favicon}',
                                  lambda _, filepath=page_builder.favicon: FileResponse(filepath)))
    if globals.config.favicon:
        add_route(None, Route(f'/static/_favicon/{globals.config.favicon}',
                              lambda _: FileResponse(globals.config.favicon)))
