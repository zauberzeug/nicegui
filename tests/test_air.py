from collections.abc import Callable
from typing import Any

import pytest
import socketio.exceptions

from nicegui import air


class FakeEngineIO:

    def __init__(self) -> None:
        self.state = 'disconnected'


class FakeRelay:
    """Minimal stand-in for ``socketio.AsyncClient`` reproducing the state semantics this module relies on.

    ``disconnect()`` only clears ``connected`` while the Engine.IO transport is still alive, because
    python-socketio clears that flag from its Engine.IO disconnect handler, which a dead transport never triggers.
    """

    def __init__(self) -> None:
        self.connected = False
        self.eio = FakeEngineIO()
        self.connect_calls = 0

    async def connect(self, *args: Any, **kwargs: Any) -> None:
        if self.connected:
            raise socketio.exceptions.ConnectionError('Already connected')
        self.connect_calls += 1
        self.connected = True
        self.eio.state = 'connected'

    async def disconnect(self) -> None:
        if self.eio.state == 'connected':
            self.connected = False
        self.eio.state = 'disconnected'

    def on(self, *args: Any, **kwargs: Any) -> Callable:
        return lambda handler: handler


@pytest.fixture
def relays(monkeypatch: pytest.MonkeyPatch) -> list[FakeRelay]:
    """Collect every relay client the ``Air`` instance creates, so a replaced client is observable."""
    created: list[FakeRelay] = []

    def create(*args: Any, **kwargs: Any) -> FakeRelay:
        created.append(FakeRelay())
        return created[-1]

    monkeypatch.setattr(air, 'timer', lambda *args, **kwargs: None)  # avoid a real keep-alive timer
    monkeypatch.setattr(air.socketio, 'AsyncClient', create)
    return created


async def test_reconnect_after_transport_died_silently(relays: list[FakeRelay]) -> None:
    instance = air.Air('token')
    instance.relay.connected = True  # the transport died without a disconnect event, leaving the flag set
    instance.relay.eio.state = 'disconnected'
    await instance.connect()
    assert sum(relay.connect_calls for relay in relays) == 1, 'a stale "connected" flag must not block the reconnect'
    assert instance.relay.connected and instance.relay.eio.state == 'connected'


async def test_no_reconnect_while_healthy(relays: list[FakeRelay]) -> None:
    instance = air.Air('token')
    instance.relay.connected = True
    instance.relay.eio.state = 'connected'
    await instance.connect()
    assert sum(relay.connect_calls for relay in relays) == 0, 'a healthy connection must not be reset'


async def test_no_reconnect_while_disconnecting(relays: list[FakeRelay]) -> None:
    instance = air.Air('token')
    instance.relay.connected = True
    instance.relay.eio.state = 'disconnecting'  # an intentional disconnect is already in progress
    await instance.connect()
    assert sum(relay.connect_calls for relay in relays) == 0, \
        'a disconnect in progress must not be reconnected by the keep-alive timer'
