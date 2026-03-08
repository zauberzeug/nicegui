"""Pyodide bridge that replaces socket.io for in-browser communication.

Instead of sending messages over a network socket, this bridge calls
JavaScript functions directly via the Pyodide FFI.
"""
from __future__ import annotations

import base64
from typing import Any


class _FakeEngineIO:
    """Fake engineio object to satisfy outbox.py's access to core.sio.eio.ping_interval/ping_timeout."""
    ping_interval = 25
    ping_timeout = 120


def _encode_bytes(obj: Any) -> Any:
    """Convert ``bytes`` values in a dict to ``{"__b64": "..."}`` for JSON serialization.

    Socket.io handles binary natively; the JSON-based Pyodide bridge does not,
    so we base64-encode bytes on the Python side and decode on the JS side.
    """
    if isinstance(obj, bytes):
        return {'__b64': base64.b64encode(obj).decode('ascii')}
    if isinstance(obj, dict):
        return {k: _encode_bytes(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_encode_bytes(item) for item in obj]
    return obj


class PyodideBridge:
    """Replaces socket.io AsyncServer for in-browser Pyodide communication.

    All emit() calls are forwarded to JavaScript via window.niceguiBridge.handleMessage().
    """

    def __init__(self) -> None:
        self.eio = _FakeEngineIO()

    async def emit(self, event: str, data: Any, room: str | None = None, **kwargs: Any) -> None:
        """Emit an event to the JavaScript frontend.

        :param event: the event type (e.g., 'update', 'run_javascript', 'notify')
        :param data: the data payload
        :param room: the target client ID (ignored in Pyodide, there's only one client)
        """
        from js import window  # type: ignore  # pylint: disable=import-outside-toplevel

        from .. import json  # pylint: disable=import-outside-toplevel
        data_json = json.dumps(_encode_bytes(data))
        # NOTE: handleMessage may return a JS Promise for async handlers (e.g. load_js_components).
        # Awaiting it ensures component JS is loaded before subsequent update messages are sent.
        result = window.niceguiBridge.handleMessage(event, data_json)
        if result is not None and hasattr(result, 'then'):
            await result
