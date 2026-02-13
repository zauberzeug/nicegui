"""Pyodide runtime — main entry point for running NiceGUI in the browser.

Usage in a PyScript/Pyodide environment::

    from nicegui import Client, ui
    from nicegui.page_pyodide import page
    from nicegui.pyodide import PyodideRuntime

    with Client(page('')) as client:
        ui.label('Hello from Pyodide!')
        ui.button('Click me!', on_click=lambda: ui.notify('Clicked!'))

    runtime = PyodideRuntime(client)
    await runtime.mount()
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

from .. import core, json
from ..dependencies import JsComponent
from .bridge import PyodideBridge
from .outbox_pyodide import PyodideOutbox

if TYPE_CHECKING:
    from ..client import Client

ELEMENTS_DIR = Path(__file__).parent.parent / 'elements'


class PyodideRuntime:
    """Runtime for running NiceGUI inside Pyodide/PyScript.

    Sets up the bridge (replacing socket.io), patches the client's outbox,
    and provides mount() to render elements into the browser DOM.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

        # NOTE: run config is normally set by ui.run / ui.run_with; in Pyodide we set defaults here
        if not core.app.config.has_run_config:
            core.app.config.add_run_config(
                reload=False,
                title='NiceGUI',
                viewport='width=device-width, initial-scale=1',
                favicon=None,
                dark=False,
                language='en-US',
                binding_refresh_interval=0.1,
                reconnect_timeout=3.0,
                message_history_length=1000,
                tailwind=True,
                unocss=None,
                prod_js=True,
                show_welcome_message=False,
            )

        # NOTE: replace socket.io with the Pyodide bridge for Python↔JS communication
        self.bridge = PyodideBridge()
        core.sio = self.bridge

        # Set up the event loop
        core.loop = asyncio.get_event_loop()

        # Replace the client's outbox with PyodideOutbox
        self.outbox = PyodideOutbox(client)
        client.outbox = self.outbox

        # Mark the client as "connected" (no real socket, but ready)
        client.tab_id = 'pyodide'
        client._temporary_socket_id = 'pyodide'

        # NOTE: start the app to trigger startup handlers (e.g. timer background tasks)
        if not core.app.is_started:
            core.app.start()

    async def mount(self) -> None:
        """Serialize all elements and send them to the JavaScript frontend for rendering."""
        from js import window  # type: ignore  # pylint: disable=import-outside-toplevel
        from pyodide.ffi import create_proxy  # type: ignore  # pylint: disable=import-outside-toplevel

        # Serialize all elements
        elements = {
            str(id): element._to_dict()  # pylint: disable=protected-access
            for id, element in self.client.elements.items()
        }
        elements_json = json.dumps(elements)

        # Collect custom Vue components that need loading before mount
        components = self._collect_components()
        components_json = json.dumps(components) if components else None

        # Register Python callbacks on the JS bridge
        window.niceguiBridge.onEvent = create_proxy(self._handle_event)
        window.niceguiBridge.onJavascriptResponse = create_proxy(self._handle_javascript_response)
        window.niceguiBridge.onUpload = create_proxy(self._handle_upload)

        # Build config for JS side (brand colors, dark mode, language)
        config = {
            'brand': core.app.config.quasar_config.get('brand', {}),
            'dark': self.client.page.resolve_dark(),
            'language': self.client.page.resolve_language(),
        }
        config_json = json.dumps(config)

        # Tell the JS side to create the NiceGUI app with our elements
        # createNiceGUIApp is async — it loads components before mounting Vue
        await window.createNiceGUIApp(elements_json, config_json, components_json)

        # Set the ready flag
        window.__pyodide_ready = True

    def _collect_components(self) -> list[dict[str, str]]:
        """Collect Vue component URLs for all elements that need custom JS components.

        Returns a list of ``{"url": "./components/...", "tag": "nicegui-..."}`` dicts
        matching the directory layout produced by ``prepare.py``.
        """
        seen: set[str] = set()
        components: list[dict[str, str]] = []
        for element in self.client.elements.values():
            comp = element.component
            if not isinstance(comp, JsComponent) or comp.name in seen:
                continue
            seen.add(comp.name)
            try:
                rel = comp.path.relative_to(ELEMENTS_DIR)
            except ValueError:
                continue
            components.append({'url': f'./components/{rel}', 'tag': comp.tag})
        return components

    async def _handle_event(self, msg_json: str) -> None:
        """Handle an event from JavaScript (e.g., button click).

        Called from JS via window.niceguiBridge.onEvent.
        When called from JS via create_proxy, the returned coroutine is
        automatically converted to a JS Promise by Pyodide.
        """
        msg = json.loads(msg_json)
        self.client.handle_event(msg)
        await self.outbox.flush()

    def _handle_javascript_response(self, msg_json: str) -> None:
        """Handle a JavaScript response (e.g., result of run_javascript).

        Called from JS via window.niceguiBridge.onJavascriptResponse.
        """
        msg = json.loads(msg_json)
        self.client.handle_javascript_response(msg)

    async def _handle_upload(self, msg_json: str) -> None:
        """Handle a file upload from JavaScript.

        Called from JS via window.niceguiBridge.onUpload.
        The upload.js factory reads files client-side and sends base64 data.
        """
        import base64  # pylint: disable=import-outside-toplevel

        from ..elements.upload import Upload  # pylint: disable=import-outside-toplevel
        from ..elements.upload_files import SmallFileUpload  # pylint: disable=import-outside-toplevel
        from ..events import UiEventArguments, handle_event  # pylint: disable=import-outside-toplevel

        msg = json.loads(msg_json)
        element_id = int(msg['id'])
        element = self.client.elements.get(element_id)
        if not isinstance(element, Upload):
            return

        for handler in element._begin_upload_handlers:
            handle_event(handler, UiEventArguments(sender=element, client=self.client))

        files = []
        for file_data in msg['files']:
            content = base64.b64decode(file_data['data'])
            files.append(SmallFileUpload(name=file_data['name'], content_type=file_data.get('type', ''), _data=content))

        await element.handle_uploads(files)
        await self.outbox.flush()
