from __future__ import annotations

import asyncio
import time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Iterable, List, Optional, Union

from fastapi import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from nicegui import json

from . import binding, globals, outbox  # pylint: disable=redefined-builtin
from .dependencies import generate_resources
from .element import Element
from .favicon import get_favicon_url
from .version import __version__

if TYPE_CHECKING:
    from .page import page

templates = Jinja2Templates(Path(__file__).parent / 'templates')


class Client:

    def __init__(self, page: page, *, shared: bool = False) -> None:
        self.id = str(uuid.uuid4())
        self.created = time.time()
        globals.clients[self.id] = self

        self.elements: Dict[int, Element] = {}
        self.next_element_id: int = 0
        self.is_waiting_for_connection: bool = False
        self.is_waiting_for_disconnect: bool = False
        self.environ: Optional[Dict[str, Any]] = None
        self.shared = shared
        self.on_air = False
        self.disconnect_task: Optional[asyncio.Task] = None

        with Element('q-layout', _client=self).props('view="hhh lpr fff"').classes('nicegui-layout') as self.layout:
            with Element('q-page-container') as self.page_container:
                with Element('q-page'):
                    self.content = Element('div').classes('nicegui-content')

        self.waiting_javascript_commands: Dict[str, Any] = {}

        self.head_html = ''
        self.body_html = ''

        self.page = page

        self.connect_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self.disconnect_handlers: List[Union[Callable[..., Any], Awaitable]] = []

    @property
    def ip(self) -> Optional[str]:
        """Return the IP address of the client, or None if the client is not connected."""
        return self.environ['asgi.scope']['client'][0] if self.environ else None  # pylint: disable=unsubscriptable-object

    @property
    def has_socket_connection(self) -> bool:
        """Return True if the client is connected, False otherwise."""
        return self.environ is not None

    def __enter__(self):
        self.content.__enter__()
        return self

    def __exit__(self, *_):
        self.content.__exit__()

    def build_response(self, request: Request, status_code: int = 200) -> Response:
        prefix = request.headers.get('X-Forwarded-Prefix', request.scope.get('root_path', ''))
        elements = json.dumps({
            id: element._to_dict() for id, element in self.elements.items()  # pylint: disable=protected-access
        })
        socket_io_js_query_params = {**globals.socket_io_js_query_params, 'client_id': self.id}
        vue_html, vue_styles, vue_scripts, imports, js_imports = generate_resources(prefix, self.elements.values())
        return templates.TemplateResponse('index.html', {
            'request': request,
            'version': __version__,
            'elements': elements.replace('&', '&amp;')
                                .replace('<', '&lt;')
                                .replace('>', '&gt;')
                                .replace('`', '&#96;'),
            'head_html': self.head_html,
            'body_html': '<style>' + '\n'.join(vue_styles) + '</style>\n' + self.body_html + '\n' + '\n'.join(vue_html),
            'vue_scripts': '\n'.join(vue_scripts),
            'imports': json.dumps(imports),
            'js_imports': '\n'.join(js_imports),
            'quasar_config': json.dumps(globals.quasar_config),
            'title': self.page.resolve_title(),
            'viewport': self.page.resolve_viewport(),
            'favicon_url': get_favicon_url(self.page, prefix),
            'dark': str(self.page.resolve_dark()),
            'language': self.page.resolve_language(),
            'prefix': prefix,
            'tailwind': globals.tailwind,
            'prod_js': globals.prod_js,
            'socket_io_js_query_params': socket_io_js_query_params,
            'socket_io_js_extra_headers': globals.socket_io_js_extra_headers,
            'socket_io_js_transports': globals.socket_io_js_transports,
        }, status_code, {'Cache-Control': 'no-store', 'X-NiceGUI-Content': 'page'})

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
        while self.id in globals.clients:
            await asyncio.sleep(check_interval)
        self.is_waiting_for_disconnect = False

    async def run_javascript(self, code: str, *,
                             respond: bool = True, timeout: float = 1.0, check_interval: float = 0.01) -> Optional[Any]:
        """Execute JavaScript on the client.

        The client connection must be established before this method is called.
        You can do this by `await client.connected()` or register a callback with `client.on_connect(...)`.
        If respond is True, the javascript code must return a string.
        """
        request_id = str(uuid.uuid4())
        command = {
            'code': code,
            'request_id': request_id if respond else None,
        }
        outbox.enqueue_message('run_javascript', command, self.id)
        if not respond:
            return None
        deadline = time.time() + timeout
        while request_id not in self.waiting_javascript_commands:
            if time.time() > deadline:
                raise TimeoutError('JavaScript did not respond in time')
            await asyncio.sleep(check_interval)
        return self.waiting_javascript_commands.pop(request_id)

    def open(self, target: Union[Callable[..., Any], str], new_tab: bool = False) -> None:
        """Open a new page in the client."""
        path = target if isinstance(target, str) else globals.page_routes[target]
        outbox.enqueue_message('open', {'path': path, 'new_tab': new_tab}, self.id)

    def download(self, url: str, filename: Optional[str] = None) -> None:
        """Download a file from the given URL."""
        outbox.enqueue_message('download', {'url': url, 'filename': filename}, self.id)

    def on_connect(self, handler: Union[Callable[..., Any], Awaitable]) -> None:
        """Register a callback to be called when the client connects."""
        self.connect_handlers.append(handler)

    def on_disconnect(self, handler: Union[Callable[..., Any], Awaitable]) -> None:
        """Register a callback to be called when the client disconnects."""
        self.disconnect_handlers.append(handler)

    def remove_elements(self, elements: Iterable[Element]) -> None:
        """Remove the given elements from the client."""
        binding.remove(elements, Element)
        element_ids = [element.id for element in elements]
        for element_id in element_ids:
            del self.elements[element_id]
        for element in elements:
            element._on_delete()  # pylint: disable=protected-access
            element._deleted = True  # pylint: disable=protected-access
            outbox.enqueue_delete(element)

    def remove_all_elements(self) -> None:
        """Remove all elements from the client."""
        self.remove_elements(self.elements.values())
