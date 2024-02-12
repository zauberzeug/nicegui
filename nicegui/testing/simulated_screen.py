
import asyncio
import functools
from queue import Empty, Queue
from typing import Callable

import pytest
from fastapi.testclient import TestClient

from nicegui import context, core, ui
from nicegui.elements.mixins.content_element import ContentElement


def app_loop(func: Callable) -> Callable:
    """Decorator to ensure a function is run in the event loop of the app."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not core.loop:
            raise RuntimeError("Event loop is not available")
        core.loop.call_soon(func, *args, **kwargs)
    return wrapper


class SimulatedScreen:

    exception_queue: Queue[Exception] = Queue()

    @app_loop
    def should_contain(self, string: str) -> None:
        """Assert that the page contains an input with the given value."""
        if self._find(context.get_client().page_container, string) is not None:
            return
        for m in context.get_client().outbox.messages:
            if m[1] == 'notify' and string in m[2]['message']:
                return
        raise AssertionError(f'text "{string}" not found on current screen')

    @app_loop
    def click(self, target_text: str) -> None:
        """Click on the element containing the given text."""
        element = self._find(context.get_client().page_container, target_text)
        assert element
        for listener in element._event_listeners.values():
            if listener.type == 'click' and listener.element_id == element.id:
                element._handle_event({'listener_id': listener.id, 'args': {}})

    def _find(self, element: ui.element, string: str) -> ui.element | None:
        text = element._text or ''
        label = element._props.get('label') or ''
        content = element.content if isinstance(element, ContentElement) else ''
        for t in [text, label, content]:
            if string in t:
                return element
        for child in element:
            found = self._find(child, string)
            if found:
                return found
        return None

    def check_exceptions(self):
        """Check if there are any exceptions in the queue and fail the test if there are."""
        try:
            exc = self.exception_queue.get_nowait()
        except Empty:
            pass
        else:
            pytest.fail(f"Exception in event loop: {exc}")
