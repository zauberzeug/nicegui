from __future__ import annotations

import asyncio
import inspect
import time
import uuid
from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Awaitable, Callable, ClassVar, Dict, Iterable, Iterator, List, Optional, Union

from fastapi import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from typing_extensions import Self

from . import background_tasks, binding, core, helpers, json, storage
from .awaitable_response import AwaitableResponse
from .dependencies import generate_resources
from .element import Element
from .favicon import get_favicon_url
from .javascript_request import JavaScriptRequest
from .logging import log
from .observables import ObservableDict
from .outbox import Outbox
from .version import __version__

if TYPE_CHECKING:
    from .page import page

templates = Jinja2Templates(Path(__file__).parent / 'templates')


class Client:
    page_routes: ClassVar[Dict[Callable[..., Any], str]] = {}
    """Maps page builders to their routes."""

    instances: ClassVar[Dict[str, Client]] = {}
    """Maps client IDs to clients."""

    auto_index_client: Client
    """The client that is used to render the auto-index page."""

    shared_head_html = ''
    """HTML to be inserted in the <head> of every page template."""

    shared_body_html = ''
    """HTML to be inserted in the <body> of every page template."""

    def __init__(self, page: page, *, request: Optional[Request]) -> None:
        self.request: Optional[Request] = request
        self.id = str(uuid.uuid4())
        self.created = time.time()
        self.instances[self.id] = self

        self.elements: Dict[int, Element] = {}
        self.next_element_id: int = 0
        self.is_waiting_for_connection: bool = False
        self.is_waiting_for_disconnect: bool = False
        self.environ: Optional[Dict[str, Any]] = None
        self.shared = request is None
        self.on_air = False
        self._num_connections: defaultdict[str, int] = defaultdict(int)
        self._delete_tasks: Dict[str, asyncio.Task] = {}
        self._deleted = False
        self._socket_to_document_id: Dict[str, str] = {}
        self.tab_id: Optional[str] = None

        self.page = page
        self.outbox = Outbox(self)

        with Element('q-layout', _client=self).props('view="hhh lpr fff"').classes('nicegui-layout') as self.layout:
            with Element('q-page-container') as self.page_container:
                with Element('q-page'):
                    self.content = Element('div').classes('nicegui-content')

        self.title: Optional[str] = None

        self._head_html = ''
        self._body_html = ''

        self.storage = ObservableDict()

        self.connect_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self.disconnect_handlers: List[Union[Callable[..., Any], Awaitable]] = []

        self._temporary_socket_id: Optional[str] = None

    @property
    def is_auto_index_client(self) -> bool:
        """Return True if this client is the auto-index client."""
        return self is self.auto_index_client

    @property
    def ip(self) -> Optional[str]:
        """Return the IP address of the client, or None if it is an
        `auto-index page <https://nicegui.io/documentation/section_pages_routing#auto-index_page>`_.

        *Updated in version 2.0.0: The IP address is available even before the client connects.*
        """
        return self.request.client.host if self.request is not None and self.request.client is not None else None

    @property
    def has_socket_connection(self) -> bool:
        """Return True if the client is connected, False otherwise."""
        return self.tab_id is not None

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
        self.outbox.updates.clear()
        prefix = request.headers.get('X-Forwarded-Prefix', request.scope.get('root_path', ''))
        elements = json.dumps({
            id: element._to_dict() for id, element in self.elements.items()  # pylint: disable=protected-access
        })
        socket_io_js_query_params = {
            **core.app.config.socket_io_js_query_params,
            'client_id': self.id,
            'next_message_id': self.outbox.next_message_id,
        }
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
                'title': self.resolve_title(),
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

    def resolve_title(self) -> str:
        """Return the title of the page."""
        return self.page.resolve_title() if self.title is None else self.title

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

    def run_javascript(self, code: str, *, timeout: float = 1.0) -> AwaitableResponse:
        """Execute JavaScript on the client.

        The client connection must be established before this method is called.
        You can do this by `await client.connected()` or register a callback with `client.on_connect(...)`.

        If the function is awaited, the result of the JavaScript code is returned.
        Otherwise, the JavaScript code is executed without waiting for a response.

        :param code: JavaScript code to run
        :param timeout: timeout in seconds (default: `1.0`)

        :return: AwaitableResponse that can be awaited to get the result of the JavaScript code
        """
        request_id = str(uuid.uuid4())
        target_id = self._temporary_socket_id or self.id

        def send_and_forget():
            self.outbox.enqueue_message('run_javascript', {'code': code}, target_id)

        async def send_and_wait():
            if self is self.auto_index_client:
                raise RuntimeError('Cannot await JavaScript responses on the auto-index page. '
                                   'There could be multiple clients connected and it is not clear which one to wait for.')
            self.outbox.enqueue_message('run_javascript', {'code': code, 'request_id': request_id}, target_id)
            return await JavaScriptRequest(request_id, timeout=timeout)

        return AwaitableResponse(send_and_forget, send_and_wait)

    def open(self, target: Union[Callable[..., Any], str], new_tab: bool = False) -> None:
        """Open a new page in the client."""
        path = target if isinstance(target, str) else self.page_routes[target]
        self.outbox.enqueue_message('open', {'path': path, 'new_tab': new_tab}, self.id)

    def download(self, src: Union[str, bytes], filename: Optional[str] = None, media_type: str = '') -> None:
        """Download a file from a given URL or raw bytes."""
        self.outbox.enqueue_message('download', {'src': src, 'filename': filename, 'media_type': media_type}, self.id)

    def on_connect(self, handler: Union[Callable[..., Any], Awaitable]) -> None:
        """Add a callback to be invoked when the client connects."""
        self.connect_handlers.append(handler)

    def on_disconnect(self, handler: Union[Callable[..., Any], Awaitable]) -> None:
        """Add a callback to be invoked when the client disconnects."""
        self.disconnect_handlers.append(handler)

    def handle_handshake(self, socket_id: str, document_id: str, next_message_id: Optional[int]) -> None:
        """Cancel pending disconnect task and invoke connect handlers."""
        self._socket_to_document_id[socket_id] = document_id
        self._cancel_delete_task(document_id)
        self._num_connections[document_id] += 1
        if next_message_id is not None:
            self.outbox.try_rewind(next_message_id)
        storage.request_contextvar.set(self.request)
        for t in self.connect_handlers:
            self.safe_invoke(t)
        for t in core.app._connect_handlers:  # pylint: disable=protected-access
            self.safe_invoke(t)

    def handle_disconnect(self, socket_id: str) -> None:
        """Wait for the browser to reconnect; invoke disconnect handlers if it doesn't.

        NOTE:
        In contrast to connect handlers, disconnect handlers are not called during a reconnect.
        This behavior should be fixed in version 3.0.
        """
        document_id = self._socket_to_document_id.pop(socket_id)
        self._cancel_delete_task(document_id)
        self._num_connections[document_id] -= 1

        async def delete_content() -> None:
            await asyncio.sleep(self.page.resolve_reconnect_timeout())
            if self._num_connections[document_id] == 0:
                for t in self.disconnect_handlers:
                    self.safe_invoke(t)
                for t in core.app._disconnect_handlers:  # pylint: disable=protected-access
                    self.safe_invoke(t)
                self._num_connections.pop(document_id)
                self._delete_tasks.pop(document_id)
                if not self.shared:
                    self.delete()
        self._delete_tasks[document_id] = background_tasks.create(delete_content())

    def _cancel_delete_task(self, document_id: str) -> None:
        if document_id in self._delete_tasks:
            self._delete_tasks.pop(document_id).cancel()

    def handle_event(self, msg: Dict) -> None:
        """Forward an event to the corresponding element."""
        with self:
            sender = self.elements.get(msg['id'])
            if sender is not None and not sender.is_ignoring_events:
                msg['args'] = [None if arg is None else json.loads(arg) for arg in msg.get('args', [])]
                if len(msg['args']) == 1:
                    msg['args'] = msg['args'][0]
                sender._handle_event(msg)  # pylint: disable=protected-access

    def handle_javascript_response(self, msg: Dict) -> None:
        """Store the result of a JavaScript command."""
        JavaScriptRequest.resolve(msg['request_id'], msg.get('result'))

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
        element_list = list(elements)  # NOTE: we need to iterate over the elements multiple times
        binding.remove(element_list)
        for element in element_list:
            element._handle_delete()  # pylint: disable=protected-access
            element._deleted = True  # pylint: disable=protected-access
            self.outbox.enqueue_delete(element)
            self.elements.pop(element.id, None)

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
        self._deleted = True

    def check_existence(self) -> None:
        """Check if the client still exists and print a warning if it doesn't."""
        if self._deleted:
            helpers.warn_once('Client has been deleted but is still being used. '
                              'This is most likely a bug in your application code. '
                              'See https://github.com/zauberzeug/nicegui/issues/3028 for more information.',
                              stack_info=True)

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
