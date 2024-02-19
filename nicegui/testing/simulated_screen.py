
from __future__ import annotations

import asyncio
import contextlib
import functools
import json
import re
from queue import Empty, Queue
from typing import Any, Callable, Dict, List, Optional, Self, Type, TypeVar, Union
from uuid import uuid4

import engineio
import httpx
import pytest
import socketio
from starlette.testclient import TestClient

import nicegui.nicegui as ng
from nicegui import Client, ElementFilter, background_tasks, context
from nicegui.awaitable_response import AwaitableResponse
from nicegui.element import Element

# pylint: disable=protected-access


class SimulatedScreen:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.http_client = client
        self.sio = socketio.AsyncClient()
        self.sio.on('connect')
        self.task = None

    async def open(self, path: str) -> User:
        """Open the given path."""
        response = await self.http_client.get(path)
        assert response.status_code == 200
        match = re.search(r"'client_id': '([0-9a-f-]+)'", response.text)
        assert match is not None
        client_id = match.group(1)
        client = Client.instances[client_id]
        await ng._on_handshake(f'test-{uuid4()}', client.id)
        return User(client)


T = TypeVar('T', bound=Element)


class User():
    current_client: Optional['Client'] = None

    def __init__(self, client: Client) -> None:
        self.client = client

    def __enter__(self) -> Self:
        self.current_client = self.client
        self.client.__enter__()
        return self

    def __exit__(self, *_) -> None:
        self.client.__exit__()
        self.current_client = None

    def should_see(self, *,
                   element: Type[T] = Element,
                   marker: Union[str, list[str], None] = None,
                   content: Union[str, list[str], None] = None,
                   ) -> AwaitableElementFilter:
        """Assert that the page contains an input with the given value."""
        return AwaitableElementFilter(check=lambda elements: len(elements) > 0, element=element, marker=marker, content=content)

    def type(self, text: str, *, element: Type[T] = Element, marker: Union[str, list[str], None] = None) -> None:
        """Type the given text into the input."""
        elements = self.should_see(element=element, marker=marker)
        element_type = element.__name__
        marker = f' with {marker=}' if marker is not None else ''
        assert len(elements) == 1, f'expected to find exactly one element of type {element_type}{marker} on the page'
        # TODO implement typing into the element; how to "submit"?

    def click(self, *,
              element: Type[T] = Element,
              marker: Union[str, list[str], None] = None,
              content: Union[str, list[str], None] = None,
              ) -> None:
        """Click the given element."""
        elements = self.should_see(element=element, marker=marker, content=content)
        element_type = element.__name__
        marker = f' with {marker=}' if marker is not None else ''
        content = f' with {content=}' if content is not None else ''
        assert len(elements) == 1, \
            f'expected to find exactly one element of type {element_type}{marker}{content} on the page'
        # TODO implement clicking the element


class AwaitableElementFilter(ElementFilter):

    def __init__(self, *,
                 check: Callable[[ElementFilter], bool],
                 element: Type = Element,
                 marker: Union[str, list[str], None] = None,
                 content: Union[str, list[str], None] = None,
                 ) -> None:
        super().__init__(element=element, marker=marker, content=content)
        self.check = check
        self._is_fired = False
        self._is_awaited = False
        self.client = context.get_client()
        background_tasks.create(self._run_check(), name='run element filter check')

    async def _run_check(self) -> ElementFilter:
        if self._is_awaited:
            return await self._check_with_retry()
        self._is_fired = True
        if self.check(self):
            return self
        else:
            raise AssertionError('not working')

    async def _check_with_retry(self) -> ElementFilter:
        with self.client:
            for _ in range(10):
                if self.check(self):
                    return self
                await asyncio.sleep(0.1)
        msg = 'not working'  # f'expected to find {type_} with {marker=}, {content=} on the page\n{self.client.layout}'
        raise AssertionError(msg)

    def __await__(self):
        if self._is_fired:
            raise RuntimeError('must be awaited immediately after creation or not at all')
        self._is_awaited = True
        return self._check_with_retry().__await__()


original_get_slot_stack = ng.Slot.get_stack
original_prune_slot_stack = ng.Slot.prune_stack


def get_stack(_=None) -> List[ng.Slot]:
    """Return the slot stack of the current client."""
    if User.current_client is None:
        return original_get_slot_stack()
    cls = ng.Slot
    client_id = id(User.current_client)
    if client_id not in cls.stacks:
        cls.stacks[client_id] = []
    return cls.stacks[client_id]


def prune_stack(cls) -> None:
    """Remove the current slot stack if it is empty."""
    if User.current_client is None:
        return original_prune_slot_stack()
    cls = ng.Slot
    client_id = id(User.current_client)
    if not cls.stacks[client_id]:
        del cls.stacks[client_id]


ng.Slot.get_stack = get_stack
ng.Slot.prune_stack = prune_stack
