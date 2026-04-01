from __future__ import annotations

from collections import defaultdict
from threading import Thread

from .. import core
from ..events import Handler, NativeEventArguments, handle_event
from . import native


class EventManager:
    """Receives pywebview window events from the subprocess and dispatches them to registered handlers."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler[NativeEventArguments]]] = defaultdict(list)
        self._thread: Thread | None = None

    def on(self, event_type: str, handler: Handler[NativeEventArguments]) -> None:
        """Register a handler for a native window event."""
        self._handlers[event_type].append(handler)

    def start(self) -> None:
        """Start the event listener thread."""
        self._thread = Thread(target=self._event_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the event listener thread."""
        if native.event_sender is not None:
            try:
                native.event_sender.send(None)
            except OSError:
                pass  # the pipe might already be closed

    def _dispatch(self, data: dict) -> None:
        args = NativeEventArguments(type=data['type'], args=data.get('args', {}))
        for handler in self._handlers.get(args.type, []):
            handle_event(handler, args)

    def _event_loop(self) -> None:
        assert native.event_receiver is not None
        while True:
            try:
                data = native.event_receiver.recv()
            except (EOFError, OSError, TypeError):
                break  # the pipe was closed
            if data is None:
                break
            if core.loop and core.loop.is_running():
                core.loop.call_soon_threadsafe(self._dispatch, data)
            else:
                self._dispatch(data)


event_manager = EventManager()
