import asyncio
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi.responses import HTMLResponse

from . import globals, ui, vue
from .element import Element
from .slot import Slot

TEMPLATE = (Path(__file__).parent / 'templates' / 'index.html').read_text()


class Client:

    def __init__(self) -> None:
        self.id = globals.next_client_id
        globals.next_client_id += 1
        globals.clients[self.id] = self

        self.elements: Dict[str, Element] = {}
        self.next_element_id: int = 0
        self.slot_stack: List[Slot] = []
        self.is_waiting_for_handshake: bool = False
        self.environ: Optional[Dict[str, Any]] = None

        globals.client_stack.append(self)
        self.content = ui.column().classes('q-ma-md')
        globals.client_stack.pop()

    def __enter__(self):
        globals.client_stack.append(self)
        self.content.__enter__()
        return self

    def __exit__(self, *_):
        self.content.__exit__()
        globals.client_stack.pop()

    def build_response(self) -> HTMLResponse:
        vue_html, vue_styles, vue_scripts = vue.generate_vue_content()
        elements = json.dumps({id: element.to_dict() for id, element in self.elements.items()})
        return HTMLResponse(TEMPLATE
                            .replace(r'{{ client_id }}', str(self.id))
                            .replace(r'{{ elements | safe }}', elements)
                            .replace(r'{{ vue_html | safe }}', vue_html)
                            .replace(r'{{ vue_styles | safe }}', vue_styles)
                            .replace(r'{{ vue_scripts | safe }}', vue_scripts)
                            .replace(r'{{ js_imports | safe }}', vue.generate_js_imports()))

    async def handshake(self, timeout: float = 3.0, check_interval: float = 0.1) -> None:
        self.is_waiting_for_handshake = True
        deadline = time.time() + timeout
        while not self.environ:
            if time.time() > deadline:
                raise TimeoutError(f'No handshake after {timeout} seconds')
            await asyncio.sleep(check_interval)
        self.is_waiting_for_handshake = False
