
import asyncio
import contextlib
import functools
import json
from queue import Empty, Queue
from typing import Any, Callable, Dict
from uuid import uuid4

import engineio
import httpx
import pytest
import socketio
from starlette.testclient import TestClient

import nicegui.nicegui as ng
from nicegui import Client, context, core, ui
from nicegui.elements.mixins.content_element import ContentElement
from nicegui.elements.mixins.source_element import SourceElement

# pylint: disable=protected-access


class SimulatedScreen:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.http_client = client
        self.sio = socketio.AsyncClient()
        self.sio.on('connect')

    async def open(self, path: str) -> Client:
        """Open the given path."""
        response = await self.http_client.get(path)
        assert response.status_code == 200
        client = list(Client.instances.values())[1]  # TODO pick the right client from the list via response
        await ng._on_handshake(f'test-{uuid4()}', client.id)
        return client

    async def should_contain(self, string: str) -> None:
        """Assert that the page contains an input with the given value."""
        for _ in range(10):
            if self._find(context.get_client().layout, string) is not None:
                return
            for m in context.get_client().outbox.messages:
                if m[1] == 'notify' and string in m[2]['message']:
                    return
            await asyncio.sleep(0.1)
        raise AssertionError(f'text "{string}" not found on current screen:\n{self}')

    def click(self, target_text: str) -> None:
        """Click on the element containing the given text."""
        element = self._find(context.get_client().layout, target_text)
        assert element
        for listener in element._event_listeners.values():
            if listener.type == 'click' and listener.element_id == element.id:
                element._handle_event({'listener_id': listener.id, 'args': {}})

    def _find(self, element: ui.element, string: str) -> ui.element | None:
        text = element._text or ''
        label = element._props.get('label') or ''
        content = element.content if isinstance(element, ContentElement) else ''
        source = element.source if isinstance(element, SourceElement) else ''
        for t in [text, label, content, source]:
            if string in t:
                return element
        for child in element:
            found = self._find(child, string)
            if found:
                return found
        return None

    def __str__(self) -> str:
        client = context.get_client()
        result = f'{client.resolve_title()}\n{client.layout}'
        for message in client.outbox.messages:
            result += f'\n{message}'
        return result
