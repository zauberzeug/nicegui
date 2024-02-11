
import functools
from typing import Callable

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

    def __init__(self, test_client: TestClient) -> None:
        self.test_client = test_client

    def open(self, path: str) -> None:
        """Open the given path."""
        response = self.test_client.get(path)
        assert response.status_code == 200

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
