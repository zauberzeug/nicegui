import asyncio
import json
import time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Dict, List, Optional, Union

from fastapi.responses import HTMLResponse

from . import globals, ui, vue
from .async_updater import AsyncUpdater
from .element import Element
from .favicon import get_favicon_url
from .slot import Slot
from .task_logger import create_task

if TYPE_CHECKING:
    from .page import page

TEMPLATE = (Path(__file__).parent / 'templates' / 'index.html').read_text()


class Client:

    def __init__(self, page: 'page') -> None:
        self.id = globals.next_client_id
        globals.next_client_id += 1
        globals.clients[self.id] = self

        self.elements: Dict[str, Element] = {}
        self.next_element_id: int = 0
        self.slot_stack: List[Slot] = []
        self.is_waiting_for_handshake: bool = False
        self.environ: Optional[Dict[str, Any]] = None

        globals.client_stack.append(self)
        with Element('q-layout').props('view="HHH LpR FFF"') as self.layout:
            with Element('q-page-container'):
                self.content = Element('div').classes('q-pa-md column items-start gap-4')
        globals.client_stack.pop()

        self.waiting_javascript_commands: Dict[str, str] = {}

        self.head_html = ''
        self.body_html = ''

        self.page = page

    @property
    def ip(self) -> Optional[str]:
        return self.environ.get('REMOTE_ADDR') if self.environ else None

    def __enter__(self):
        globals.client_stack.append(self)
        self.content.__enter__()
        return self

    def __exit__(self, *_):
        self.content.__exit__()
        globals.client_stack.pop()

    def watch_asyncs(self, coro: Coroutine) -> AsyncUpdater:
        return AsyncUpdater(coro, self)

    def build_response(self) -> HTMLResponse:
        vue_html, vue_styles, vue_scripts = vue.generate_vue_content()
        elements = json.dumps({id: element.to_dict() for id, element in self.elements.items()})
        return HTMLResponse(
            TEMPLATE
            .replace(r'{{ client_id }}', str(self.id))
            .replace(r'{{ socket_address }}', f'ws://{globals.host}:{globals.port}')
            .replace(r'{{ elements | safe }}', elements)
            .replace(r'{{ head_html | safe }}', self.head_html)
            .replace(r'{{ body_html | safe }}', f'{self.body_html}\n{vue_html}\n{vue_styles}')
            .replace(r'{{ vue_scripts | safe }}', vue_scripts)
            .replace(r'{{ js_imports | safe }}', vue.generate_js_imports())
            .replace(r'{{ title }}', self.page.resolve_title())
            .replace(r'{{ favicon_url }}', get_favicon_url(self.page))
            .replace(r'{{ dark }}', str(self.page.resolve_dark()))
        )

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
        create_task(globals.sio.emit('run_javascript', command, room=str(self.id)))
        if not respond:
            return
        deadline = time.time() + timeout
        while request_id not in self.waiting_javascript_commands:
            if time.time() > deadline:
                raise TimeoutError('JavaScript did not respond in time')
            await asyncio.sleep(check_interval)
        return self.waiting_javascript_commands.pop(request_id)

    def open(self, target: Union[Callable, str]) -> None:
        path = target if isinstance(target, str) else globals.page_routes[target]
        create_task(globals.sio.emit('open', path, room=str(self.id)))


class ErrorClient(Client):

    def __init__(self, page: 'page') -> None:
        super().__init__(page)
        with self:
            with ui.column().classes('w-full py-20 items-center gap-0'):
                ui.icon('☹').classes('text-8xl py-5') \
                    .style('font-family: "Arial Unicode MS", "Times New Roman", Times, serif;')
                self.status_code = ui.label().classes('text-6xl py-5')
                self.title = ui.label().classes('text-xl py-5')
                self.message = ui.label().classes('text-lg py-2 text-gray-500')

    def build_response(self, status_code: int, message: str = '') -> HTMLResponse:
        self.status_code.text = status_code
        if 400 <= status_code <= 499:
            self.title.text = "This page doesn't exist"
        elif 500 <= status_code <= 599:
            self.title.text = 'Server error'
        else:
            self.title.text = 'Unknown error'
        self.message.text = message
        return super().build_response()
