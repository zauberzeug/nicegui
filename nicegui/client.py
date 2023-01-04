import asyncio
import json
import time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, List, Optional, Union

from fastapi import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from . import globals
from .dependencies import generate_js_imports, generate_vue_content
from .element import Element
from .favicon import get_favicon_url
from .task_logger import create_task

if TYPE_CHECKING:
    from .page import page

templates = Jinja2Templates(Path(__file__).parent / 'templates')


class Client:

    def __init__(self, page: 'page', *, shared: bool = False) -> None:
        self.id = str(uuid.uuid4())
        self.created = time.time()
        globals.clients[self.id] = self

        self.elements: Dict[int, Element] = {}
        self.next_element_id: int = 0
        self.is_waiting_for_handshake: bool = False
        self.environ: Optional[Dict[str, Any]] = None
        self.shared = shared

        with Element('q-layout', _client=self).props('view="HHH LpR FFF"') as self.layout:
            with Element('q-page-container'):
                with Element('q-page'):
                    self.content = Element('div').classes('q-pa-md column items-start gap-4')

        self.waiting_javascript_commands: Dict[str, str] = {}

        self.head_html = ''
        self.body_html = ''

        self.page = page

        self.connect_handlers: List[Union[Callable, Awaitable]] = []
        self.disconnect_handlers: List[Union[Callable, Awaitable]] = []

    @property
    def ip(self) -> Optional[str]:
        return self.environ.get('REMOTE_ADDR') if self.environ else None

    @property
    def has_socket_connection(self) -> bool:
        return self.environ is not None

    def __enter__(self):
        self.content.__enter__()
        return self

    def __exit__(self, *_):
        self.content.__exit__()

    def build_response(self, request: Request, status_code: int = 200) -> Response:
        prefix = request.headers.get('X-Forwarded-Prefix', '')
        vue_html, vue_styles, vue_scripts = generate_vue_content()
        elements = json.dumps({id: element.to_dict() for id, element in self.elements.items()})
        return templates.TemplateResponse('index.html', {
            'request': request,
            'client_id': str(self.id),
            'elements': elements,
            'head_html': self.head_html,
            'body_html': f'{self.body_html}\n{vue_html}\n{vue_styles}',
            'vue_scripts': vue_scripts,
            'js_imports': generate_js_imports(prefix),
            'title': self.page.resolve_title(),
            'favicon_url': get_favicon_url(self.page, prefix),
            'dark': str(self.page.resolve_dark()),
            'prefix': prefix,
            'socket_io_js_extra_headers': globals.socket_io_js_extra_headers,
        }, status_code, {'Cache-Control': 'no-store', 'X-NiceGUI-Content': 'page'})

    async def handshake(self, timeout: float = 3.0, check_interval: float = 0.1) -> None:
        self.is_waiting_for_handshake = True
        deadline = time.time() + timeout
        while not self.environ:
            if time.time() > deadline:
                raise TimeoutError(f'No handshake after {timeout} seconds')
            await asyncio.sleep(check_interval)
        self.is_waiting_for_handshake = False

    async def run_javascript(self, code: str, *,
                             respond: bool = True, timeout: float = 1.0, check_interval: float = 0.01) -> Optional[str]:
        request_id = str(uuid.uuid4())
        command = {
            'code': code,
            'request_id': request_id if respond else None,
        }
        create_task(globals.sio.emit('run_javascript', command, room=self.id))
        if not respond:
            return None
        deadline = time.time() + timeout
        while request_id not in self.waiting_javascript_commands:
            if time.time() > deadline:
                raise TimeoutError('JavaScript did not respond in time')
            await asyncio.sleep(check_interval)
        return self.waiting_javascript_commands.pop(request_id)

    def open(self, target: Union[Callable, str]) -> None:
        path = target if isinstance(target, str) else globals.page_routes[target]
        create_task(globals.sio.emit('open', path, room=self.id))
