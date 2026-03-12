from __future__ import annotations

import asyncio
import inspect
import time
import uuid
from collections import defaultdict
from collections.abc import Awaitable, Callable, Iterable
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, cast

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
from .sub_pages_router import SubPagesRouter
from .translations import translations
from .version import __version__

if TYPE_CHECKING:
    from .page import page

templates = Jinja2Templates(Path(__file__).parent / 'templates')

HTML_ESCAPE_TABLE = str.maketrans({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '`': '&#96;',
    '$': '&#36;',
})

HEADWIND_CONTENT = (Path(__file__).parent / 'static' / 'headwind.css').read_text().strip()


class ClientConnectionTimeout(TimeoutError):
    def __init__(self, client: Client) -> None:
        super().__init__(f'ClientConnectionTimeout: {client.id}')
        self.client = client


class Client:
    page_routes: ClassVar[dict[Callable[..., Any], str]] = {}
    '''Maps page builders to their routes.'''

    instances: ClassVar[dict[str, Client]] = {}
    '''Maps client IDs to clients.'''

    shared_head_html = ''
    '''HTML to be inserted in the <head> of every page template.'''

    shared_body_html = ''
    '''HTML to be inserted in the <body> of every page template.'''

    def __init__(self, page: page, *, request: Request | None = None) -> None:
        self._request = request
        self.id = str(uuid.uuid4())
        self.created = time.time()
        self.instances[self.id] = self

        self.elements: dict[int, Element] = {}
        self.next_element_id: int = 0
        self._waiting_for_connection = asyncio.Event()
        self._waiting_for_disconnect = asyncio.Event()
        self._connected = asyncio.Event()
        self._deleted_event = asyncio.Event()
        self.environ: dict[str, Any] | None = None
        self.on_air = False
        self._num_connections: defaultdict[str, int] = defaultdict(int)
        self._delete_tasks: dict[str, asyncio.Task] = {}
        self._deleted = False
        self._socket_to_document_id: dict[str, str] = {}
        self.tab_id: str | None = None
        self._exception_handlers: list[Callable[[Exception], Any] | Callable[[], Any]] = []

        self.page = page
        self.outbox = Outbox(self)

        if self._request is not None:
            self._request.scope['nicegui_page_path'] = self.page.path

        with Element('q-layout', _client=self).props('view="hhh lpr fff"').classes('nicegui-layout') as self.layout:
            with Element('q-page-container') as self.page_container:
                with Element('q-page'):
                    self.content = Element('div').classes('nicegui-content')

        self.title: str | None = None

        self._head_html = ''
        self._body_html = ''

        self.storage = ObservableDict()

        self.connect_handlers: list[Callable[..., Any] | Awaitable] = []
        self.disconnect_handlers: list[Callable[..., Any] | Awaitable] = []
        self.delete_handlers: list[Callable[..., Any] | Awaitable] = []

        self._temporary_socket_id: str | None = None

        with self:
            self.sub_pages_router = SubPagesRouter(request)

    @property
    def request(self) -> Request:
        """The request object for the client."""
        if self._request is None:
            raise RuntimeError('Request is not set')
        return self._request

    @property
    def ip(self) -> str:
        """The IP address of the client.

        *Updated in version 2.0.0: The IP address is available even before the client connects.*
        *Updated in version 3.0.0: The IP address is always defined (never ``None``).*
        """
        return self.request.client.host if self.request.client is not None else ''

    @property
    def has_socket_connection(self) -> bool:
        """Whether the client is connected."""
        return self.tab_id is not None

    @property
    def head_html(self) -> str:
        """The HTML code to be inserted in the <head> of the page template."""
        return self.shared_head_html + self._head_html

    @property
    def body_html(self) -> str:
        """The HTML code to be inserted in the <body> of the page template."""
        return self.shared_body_html + self._body_html

    def __enter__(self) -> Self:
        self.content.__enter__()
        return self

    def __exit__(self, *_) -> None:
        self.content.__exit__()

    def build_response(self, request: Request, status_code: int = 200) -> Response:
        """Build a FastAPI response for the client."""
        self.outbox.updates.clear()
        prefix = request.headers.get('X-Forwarded-Prefix', '') + request.scope.get('root_path', '')
        elements = json.dumps({
            id: element._to_dict() for id, element in self.elements.items()  # pylint: disable=protected-access
        })
        socket_io_js_query_params = {
            **core.app.config.socket_io_js_query_params,
            'client_id': self.id,
            'next_message_id': self.outbox.next_message_id,
            'implicit_handshake': not _is_prefetch(request),
        }
        vue_html, vue_styles, vue_scripts, imports, js_imports, js_imports_urls = \
            generate_resources(prefix, self.elements.values())
        return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={
                'request': request,
                'version': __version__,
                'elements': elements.translate(HTML_ESCAPE_TABLE),
                'head_html': self.head_html,
                'body_html': '<style>' + '\n'.join(vue_styles) + '</style>\n' + self.body_html + '\n' + '\n'.join(vue_html),
                'vue_scripts': '\n'.join(vue_scripts),
                'imports': json.dumps(imports),
                'js_imports': '\n'.join(js_imports),
                'js_imports_urls': js_imports_urls,
                'vue_config': json.dumps(core.app.config.quasar_config),
                'vue_config_script': core.app.config.vue_config_script,
                'title': self.resolve_title(),
                'viewport': self.page.resolve_viewport(),
                'favicon_url': get_favicon_url(self.page, prefix),
                'dark': str(self.page.resolve_dark()),
                'language': self.page.resolve_language(),
                'translations': translations.get(self.page.resolve_language(), translations['en-US']),
                'prefix': prefix,
                'tailwind': core.app.config.tailwind,
                'unocss': core.app.config.unocss,
                'headwind_css': HEADWIND_CONTENT if core.app.config.tailwind else '',
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

    async def connected(self, timeout: float | None = None) -> None:
        """Block execution until the client is connected.

        :param timeout: timeout in seconds (default: ``None``)
        """
        if self.has_socket_connection:
            return
        self._waiting_for_connection.set()
        self._connected.clear()
        try:
            await asyncio.wait_for(self._connected.wait(), timeout=None if _is_prefetch(self.request) else timeout)
        except asyncio.TimeoutError as e:
            raise ClientConnectionTimeout(self) from e

    async def disconnected(self) -> None:
        """Block execution until the client disconnects."""
        if not self.has_socket_connection:
            await self.connected()
        if self.id in self.instances:
            self._waiting_for_disconnect.set()
            self._deleted_event.clear()
            await self._deleted_event.wait()

    def run_javascript(self, code: str, *, timeout: float = 1.0) -> AwaitableResponse:
        """Execute JavaScript on the client.

        If the function is awaited, the result of the JavaScript code is returned.
        Otherwise, the JavaScript code is executed without waiting for a response.

        Obviously the JavaScript code is only executed after the client is connected.
        Internally, ``await client.connected()`` is called before the JavaScript code is executed (*since version 3.0.0*).
        This might delay the execution of the JavaScript code and is not covered by the ``timeout`` parameter.

        :param code: JavaScript code to run
        :param timeout: timeout in seconds (default: 1.0)

        :return: AwaitableResponse that can be awaited to get the result of the JavaScript code
        """
        request_id = str(uuid.uuid4())
        target_id = self._temporary_socket_id or self.id

        def send_and_forget():
            self.outbox.enqueue_message('run_javascript', {'code': code}, target_id)

        async def send_and_wait():
            self.outbox.enqueue_message('run_javascript', {'code': code, 'request_id': request_id}, target_id)
            await self.connected()
            return await JavaScriptRequest(request_id, timeout=timeout)

        return AwaitableResponse(send_and_forget, send_and_wait)

    def open(self, target: Callable[..., Any] | str, new_tab: bool = False) -> None:
        """Open a new page in the client."""
        path = target if isinstance(target, str) else self.page_routes[target]
        self.outbox.enqueue_message('open', {'path': path, 'new_tab': new_tab}, self.id)

    def download(self, src: str | bytes, filename: str | None = None, media_type: str = '') -> None:
        """Download a file from a given URL or raw bytes."""
        self.outbox.enqueue_message('download', {'src': src, 'filename': filename, 'media_type': media_type}, self.id)

    def on_connect(self, handler: Callable[..., Any] | Awaitable) -> None:
        """Add a callback to be invoked when the client connects.

        The callback has an optional parameter of `nicegui.Client`.
        """
        self.connect_handlers.append(handler)

    def on_disconnect(self, handler: Callable[..., Any] | Awaitable) -> None:
        """Add a callback to be invoked when the client disconnects.

        The callback has an optional parameter of `nicegui.Client`.

        *Updated in version 3.0.0: The handler is also called when a client reconnects.*
        """
        self.disconnect_handlers.append(handler)

    def on_delete(self, handler: Callable[..., Any] | Awaitable) -> None:
        """Add a callback to be invoked when the client is deleted.

        The callback has an optional parameter of `nicegui.Client`.

        *Added in version 3.0.0*
        """
        self.delete_handlers.append(handler)

    def on_exception(self, handler: Callable[[Exception], Any] | Callable[[], Any]) -> None:
        """Add a callback to be invoked for in-page exceptions (after the page has been sent to the browser).

        The callback has an optional parameter of `Exception`.
        """
        self._exception_handlers.append(handler)

    def handle_handshake(self, socket_id: str, document_id: str, next_message_id: int | None) -> None:
        """Cancel pending disconnect task and invoke connect handlers. (For internal use only.)"""
        self._waiting_for_connection.clear()
        self._connected.set()
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
        """Wait for the browser to reconnect; invoke deletion handlers if it doesn't. (For internal use only.)"""
        if socket_id not in self._socket_to_document_id:
            return
        document_id = self._socket_to_document_id.pop(socket_id)
        self._cancel_delete_task(document_id)
        self._num_connections[document_id] -= 1
        tab_id_to_close = self.tab_id
        self.tab_id = None

        for t in self.disconnect_handlers:
            self.safe_invoke(t)
        for t in core.app._disconnect_handlers:  # pylint: disable=protected-access
            self.safe_invoke(t)

        async def delete_content() -> None:
            await asyncio.sleep(self.page.resolve_reconnect_timeout())
            if self._num_connections[document_id] == 0:
                self._num_connections.pop(document_id)
                self._delete_tasks.pop(document_id)
                await core.app.storage.close_tab(tab_id_to_close)
                self.delete()
        self._delete_tasks[document_id] = \
            background_tasks.create(delete_content(), name=f'delete content {document_id}')

    def _cancel_delete_task(self, document_id: str) -> None:
        if document_id in self._delete_tasks:
            self._delete_tasks.pop(document_id).cancel()

    def handle_event(self, msg: dict) -> None:
        """Forward an event to the corresponding element. (For internal use only.)"""
        with self:
            sender = self.elements.get(msg['id'])
            if sender is not None and not sender.is_ignoring_events:
                msg['args'] = [None if arg is None else json.loads(arg) for arg in msg.get('args', [])]
                if len(msg['args']) == 1:
                    msg['args'] = msg['args'][0]
                sender._handle_event(msg)  # pylint: disable=protected-access

    def handle_log_message(self, msg: dict) -> None:
        """Log a message from the client. (For internal use only.)"""
        {
            'debug': log.debug,
            'info': log.info,
            'warning': log.warning,
            'error': log.error,
        }[msg['level']](msg['message'])

    def handle_javascript_response(self, msg: dict) -> None:
        """Store the result of a JavaScript command. (For internal use only.)"""
        JavaScriptRequest.resolve(msg['request_id'], msg.get('result'))

    def safe_invoke(self, func: Callable[..., Any] | Awaitable) -> None:
        """Invoke the potentially async function in the client context and catch any exceptions."""
        func_name = func.__name__ if hasattr(func, '__name__') else str(func)
        try:
            if isinstance(func, Awaitable):
                async def func_with_client():
                    with self:
                        await func
                background_tasks.create(func_with_client(), name=f'func with client {self.id} {func_name}')
            else:
                with self:
                    result = func(self) if len(inspect.signature(func).parameters) == 1 else func()
                if helpers.is_coroutine_function(func) and not isinstance(result, asyncio.Task):
                    async def result_with_client():
                        with self:
                            await result
                    background_tasks.create(result_with_client(), name=f'result with client {self.id} {func_name}')
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

    def handle_exception(self, exception: Exception) -> None:
        """Handle an in-page exception by invoking handlers registered via `ui.on_exception(...)`."""
        for handler in self._exception_handlers:
            with self.content:
                if helpers.expects_arguments(handler):
                    result = cast(Callable[[Exception], Any], handler)(exception)
                else:
                    result = cast(Callable[[], Any], handler)()
            if helpers.is_coroutine_function(handler):
                async def wait_for_result(result: Any = result) -> None:
                    with self.content:
                        await result
                background_tasks.create(wait_for_result(), name=f'UI exception {handler.__name__}')

    def delete(self) -> None:
        """Delete a client and all its elements.

        If the global clients dictionary does not contain the client, its elements are still removed and a KeyError is raised.
        Normally this should never happen, but has been observed (see #1826).
        """
        for t in self.delete_handlers:
            self.safe_invoke(t)
        for t in core.app._delete_handlers:  # pylint: disable=protected-access
            self.safe_invoke(t)
        self._waiting_for_disconnect.clear()
        self._deleted_event.set()
        self.remove_all_elements()
        self.outbox.stop()
        del Client.instances[self.id]
        self._deleted = True
        self._connected.set()  # for terminating connected() waits
        self._connected.clear()

    def check_existence(self) -> None:
        """Check if the client still exists and print a warning if it doesn't."""
        if self._deleted:
            helpers.warn_once('Client has been deleted but is still being used. '
                              'This is most likely a bug in your application code. '
                              'See https://github.com/zauberzeug/nicegui/issues/3028 for more information.',
                              stack_info=True)

    @classmethod
    def prune_instances(cls, *, client_age_threshold: float = 60.0) -> None:
        """Prune stale clients."""
        try:
            stale_clients = [
                client
                for client in cls.instances.values()
                if (
                    not client.has_socket_connection and
                    not client._delete_tasks and  # pylint: disable=protected-access
                    client.created <= time.time() - client_age_threshold
                )
            ]
            for client in stale_clients:
                log.debug(f'Pruning stale client {client.id}')
                client.delete()

        except Exception:
            log.exception('Error while pruning clients')


def _is_prefetch(request: Request) -> bool:
    purpose = (request.headers.get('Sec-Purpose') or request.headers.get('Purpose') or '').lower()
    return 'prefetch' in purpose and 'prerender' not in purpose
