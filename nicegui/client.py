from __future__ import annotations

import asyncio
import inspect
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Iterable, Iterator, List, Optional, Union

from fastapi import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from typing_extensions import Self

from . import background_tasks, binding, core, helpers, json
from .awaitable_response import AwaitableResponse
from .dependencies import generate_resources
from .element import Element
from .favicon import get_favicon_url
from .logging import log
from .outbox import Outbox
from .version import __version__

if TYPE_CHECKING:
    from .page import page

templates = Jinja2Templates(Path(__file__).parent / 'templates')


class Client:
    page_routes: Dict[Callable[..., Any], str] = {}
    """Maps page builders to their routes."""

    instances: Dict[str, Client] = {}
    """Maps client IDs to clients."""

    auto_index_client: Client
    """The client that is used to render the auto-index page."""

    shared_head_html = ''
    """HTML to be inserted in the <head> of every page template."""

    shared_body_html = ''
    """HTML to be inserted in the <body> of every page template."""

    def __init__(self, page: page, *, shared: bool = False) -> None:
        self.id = str(uuid.uuid4())
        self.created = time.time()
        self.instances[self.id] = self

        self.elements: Dict[int, Element] = {}
        self.next_element_id: int = 0
        self.is_waiting_for_connection: bool = False
        self.is_waiting_for_disconnect: bool = False
        self.environ: Optional[Dict[str, Any]] = None
        self.shared = shared
        self.on_air = False
        self._disconnect_task: Optional[asyncio.Task] = None

        self.outbox = Outbox(self)

        with Element('q-layout', _client=self).props('view="hhh lpr fff"').classes('nicegui-layout') as self.layout:
            with Element('q-page-container') as self.page_container:
                with Element('q-page'):
                    self.content = Element('div').classes('nicegui-content')

        self.waiting_javascript_commands: Dict[str, Any] = {}

        self.title: Optional[str] = None

        self._head_html = ''
        self._body_html = ''

        self.page = page

        self.connect_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self.disconnect_handlers: List[Union[Callable[..., Any], Awaitable]] = []

        self._temporary_socket_id: Optional[str] = None

    @property
    def is_auto_index_client(self) -> bool:
        """Return True if this client is the auto-index client."""
        return self is self.auto_index_client

    @property
    def ip(self) -> Optional[str]:
        """Return the IP address of the client, or None if the client is not connected."""
        return self.environ['asgi.scope']['client'][0] if self.environ else None  # pylint: disable=unsubscriptable-object

    @property
    def has_socket_connection(self) -> bool:
        """Return True if the client is connected, False otherwise."""
        return self.environ is not None

    @property
    def head_html(self) -> str:
        """Return the HTML code to be inserted in the <head> of the page template."""
        return self.shared_head_html + self._head_html

    @property
    def body_html(self) -> str:
        """Return the HTML code to be inserted in the <body> of the page template."""
        return self.shared_body_html + self._body_html

    def __enter__(self) -> Self:
        self.content.__enter__()
        return self

    def __exit__(self, *_) -> None:
        self.content.__exit__()

    def build_response(self, request: Request, status_code: int = 200) -> Response:
        """Build a FastAPI response for the client."""
        prefix = request.headers.get('X-Forwarded-Prefix', request.scope.get('root_path', ''))
        elements = json.dumps({
            id: element._to_dict() for id, element in self.elements.items()  # pylint: disable=protected-access
        })
        socket_io_js_query_params = {**core.app.config.socket_io_js_query_params, 'client_id': self.id}
        vue_html, vue_styles, vue_scripts, imports, js_imports = generate_resources(prefix, self.elements.values())
        return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={
                'request': request,
                'version': __version__,
                'elements': elements.replace('&', '&amp;')
                                    .replace('<', '&lt;')
                                    .replace('>', '&gt;')
                                    .replace('`', '&#96;')
                                    .replace('$', '&#36;'),
                'head_html': self.head_html,
                'body_html': '<style>' + '\n'.join(vue_styles) + '</style>\n' + self.body_html + '\n' + '\n'.join(vue_html),
                'vue_scripts': '\n'.join(vue_scripts),
                'imports': json.dumps(imports),
                'js_imports': '\n'.join(js_imports),
                'quasar_config': json.dumps(core.app.config.quasar_config),
                'title': self.page.resolve_title() if self.title is None else self.title,
                'viewport': self.page.resolve_viewport(),
                'favicon_url': get_favicon_url(self.page, prefix),
                'dark': str(self.page.resolve_dark()),
                'language': self.page.resolve_language(),
                'prefix': prefix,
                'tailwind': core.app.config.tailwind,
                'prod_js': core.app.config.prod_js,
                'socket_io_js_query_params': socket_io_js_query_params,
                'socket_io_js_extra_headers': core.app.config.socket_io_js_extra_headers,
                'socket_io_js_transports': core.app.config.socket_io_js_transports,
            },
            status_code=status_code,
            headers={'Cache-Control': 'no-store', 'X-NiceGUI-Content': 'page'},
        )

    async def connected(self, timeout: float = 3.0, check_interval: float = 0.1) -> None:
        """Block execution until the client is connected."""
        self.is_waiting_for_connection = True
        deadline = time.time() + timeout
        while not self.has_socket_connection:
            if time.time() > deadline:
                raise TimeoutError(f'No connection after {timeout} seconds')
            await asyncio.sleep(check_interval)
        self.is_waiting_for_connection = False

    async def disconnected(self, check_interval: float = 0.1) -> None:
        """Block execution until the client disconnects."""
        if not self.has_socket_connection:
            await self.connected()
        self.is_waiting_for_disconnect = True
        while self.id in self.instances:
            await asyncio.sleep(check_interval)
        self.is_waiting_for_disconnect = False

    def run_javascript(self, code: str, *,
                       respond: Optional[bool] = None,  # DEPRECATED
                       timeout: float = 1.0, check_interval: float = 0.01) -> AwaitableResponse:
        """Execute JavaScript on the client.

        The client connection must be established before this method is called.
        You can do this by `await client.connected()` or register a callback with `client.on_connect(...)`.

        If the function is awaited, the result of the JavaScript code is returned.
        Otherwise, the JavaScript code is executed without waiting for a response.

        :param code: JavaScript code to run
        :param timeout: timeout in seconds (default: `1.0`)
        :param check_interval: interval in seconds to check for a response (default: `0.01`)

        :return: AwaitableResponse that can be awaited to get the result of the JavaScript code
        """
        if respond is True:
            log.warning('The "respond" argument of run_javascript() has been removed. '
                        'Now the method always returns an AwaitableResponse that can be awaited. '
                        'Please remove the "respond=True" argument.')
        if respond is False:
            raise ValueError('The "respond" argument of run_javascript() has been removed. '
                             'Now the method always returns an AwaitableResponse that can be awaited. '
                             'Please remove the "respond=False" argument and call the method without awaiting.')

        request_id = str(uuid.uuid4())
        target_id = self._temporary_socket_id or self.id

        def send_and_forget():
            self.outbox.enqueue_message('run_javascript', {'code': code}, target_id)

        async def send_and_wait():
            self.outbox.enqueue_message('run_javascript', {'code': code, 'request_id': request_id}, target_id)
            deadline = time.time() + timeout
            while request_id not in self.waiting_javascript_commands:
                if time.time() > deadline:
                    raise TimeoutError(f'JavaScript did not respond within {timeout:.1f} s')
                await asyncio.sleep(check_interval)
            return self.waiting_javascript_commands.pop(request_id)

        return AwaitableResponse(send_and_forget, send_and_wait)

    def open(self, target: Union[Callable[..., Any], str], new_tab: bool = False) -> None:
        """Open a new page in the client."""
        path = target if isinstance(target, str) else self.page_routes[target]
        self.outbox.enqueue_message('open', {'path': path, 'new_tab': new_tab}, self.id)

    def download(self, src: Union[str, bytes], filename: Optional[str] = None, media_type: str = '') -> None:
        """Download a file from a given URL or raw bytes."""
        self.outbox.enqueue_message('download', {'src': src, 'filename': filename, 'media_type': media_type}, self.id)

    def on_connect(self, handler: Union[Callable[..., Any], Awaitable]) -> None:
        """Register a callback to be called when the client connects."""
        self.connect_handlers.append(handler)

    def on_disconnect(self, handler: Union[Callable[..., Any], Awaitable]) -> None:
        """Register a callback to be called when the client disconnects."""
        self.disconnect_handlers.append(handler)

    def handle_handshake(self) -> None:
        """Cancel pending disconnect task and invoke connect handlers."""
        if self._disconnect_task:
            self._disconnect_task.cancel()
            self._disconnect_task = None
        for t in self.connect_handlers:
            self.safe_invoke(t)
        for t in core.app._connect_handlers:  # pylint: disable=protected-access
            self.safe_invoke(t)

    def handle_disconnect(self) -> None:
        """Wait for the browser to reconnect; invoke disconnect handlers if it doesn't."""
        async def handle_disconnect() -> None:
            if self.page.reconnect_timeout is not None:
                delay = self.page.reconnect_timeout
            else:
                delay = core.app.config.reconnect_timeout  # pylint: disable=protected-access
            await asyncio.sleep(delay)
            for t in self.disconnect_handlers:
                self.safe_invoke(t)
            for t in core.app._disconnect_handlers:  # pylint: disable=protected-access
                self.safe_invoke(t)
            if not self.shared:
                self.delete()
        self._disconnect_task = background_tasks.create(handle_disconnect())

    def handle_event(self, msg: Dict) -> None:
        """Forward an event to the corresponding element."""
        with self:
            sender = self.elements.get(msg['id'])
            if sender is not None:
                msg['args'] = [None if arg is None else json.loads(arg) for arg in msg.get('args', [])]
                if len(msg['args']) == 1:
                    msg['args'] = msg['args'][0]
                sender._handle_event(msg)  # pylint: disable=protected-access

    def handle_javascript_response(self, msg: Dict) -> None:
        """Store the result of a JavaScript command."""
        self.waiting_javascript_commands[msg['request_id']] = msg['result']

    def safe_invoke(self, func: Union[Callable[..., Any], Awaitable]) -> None:
        """Invoke the potentially async function in the client context and catch any exceptions."""
        try:
            if isinstance(func, Awaitable):
                async def func_with_client():
                    with self:
                        await func
                background_tasks.create(func_with_client())
            else:
                with self:
                    result = func(self) if len(inspect.signature(func).parameters) == 1 else func()
                if helpers.is_coroutine_function(func):
                    async def result_with_client():
                        with self:
                            await result
                    background_tasks.create(result_with_client())
        except Exception as e:
            core.app.handle_exception(e)

    def remove_elements(self, elements: Iterable[Element]) -> None:
        """Remove the given elements from the client."""
        binding.remove(elements)
        element_ids = [element.id for element in elements]
        for element in elements:
            element._handle_delete()  # pylint: disable=protected-access
            element._deleted = True  # pylint: disable=protected-access
            self.outbox.enqueue_delete(element)
        for element_id in element_ids:
            del self.elements[element_id]

    def remove_all_elements(self) -> None:
        """Remove all elements from the client."""
        self.remove_elements(self.elements.values())

    def delete(self) -> None:
        """Delete a client and all its elements.

        If the global clients dictionary does not contain the client, its elements are still removed and a KeyError is raised.
        Normally this should never happen, but has been observed (see #1826).
        """
        self.remove_all_elements()
        self.outbox.stop()
        del Client.instances[self.id]

    @contextmanager
    def individual_target(self, socket_id: str) -> Iterator[None]:
        """Use individual socket ID while in this context.

        This context is useful for limiting messages from the shared auto-index page to a single client.
        """
        self._temporary_socket_id = socket_id
        yield
        self._temporary_socket_id = None

    @classmethod
    async def prune_instances(cls) -> None:
        """Prune stale clients in an endless loop."""
        while True:
            try:
                stale_clients = [
                    client
                    for client in cls.instances.values()
                    if not client.shared and not client.has_socket_connection and client.created < time.time() - 60.0
                ]
                for client in stale_clients:
                    client.delete()
            except Exception:
                # NOTE: make sure the loop doesn't crash
                log.exception('Error while pruning clients')
            await asyncio.sleep(10)
