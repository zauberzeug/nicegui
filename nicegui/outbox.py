from __future__ import annotations

import asyncio
from collections import deque
from typing import TYPE_CHECKING, Any, Deque, Dict, Optional, Tuple

from . import background_tasks, core

if TYPE_CHECKING:
    from .client import Client
    from .element import Element

ClientId = str
ElementId = int
MessageType = str
Message = Tuple[ClientId, MessageType, Any]


class Outbox:

    def __init__(self, client: Client) -> None:
        self.client = client
        self.updates: Dict[ElementId, Optional[Element]] = {}
        self.messages: Deque[Message] = deque()
        self._should_stop = False
        self._enqueue_event: Optional[asyncio.Event] = None
        if core.app.is_started:
            background_tasks.create(self.loop(), name=f'outbox loop {client.id}')
        else:
            core.app.on_startup(self.loop)

    def _set_enqueue_event(self) -> None:
        """Set the enqueue event while accounting for lazy initialization."""
        if self._enqueue_event:
            self._enqueue_event.set()

    def enqueue_update(self, element: Element) -> None:
        """Enqueue an update for the given element."""
        self.updates[element.id] = element
        self._set_enqueue_event()

    def enqueue_delete(self, element: Element) -> None:
        """Enqueue a deletion for the given element."""
        self.updates[element.id] = None
        self._set_enqueue_event()

    def enqueue_message(self, message_type: MessageType, data: Any, target_id: ClientId) -> None:
        """Enqueue a message for the given client."""
        self.messages.append((target_id, message_type, data))
        self._set_enqueue_event()

    async def loop(self) -> None:
        """Send updates and messages to all clients in an endless loop."""
        self._enqueue_event = asyncio.Event()
        self._enqueue_event.set()

        while not self._should_stop:
            try:
                if not self._enqueue_event.is_set():
                    try:
                        await asyncio.wait_for(self._enqueue_event.wait(), timeout=1.0)
                    except (TimeoutError, asyncio.TimeoutError):
                        continue

                if not self.client.has_socket_connection:
                    await asyncio.sleep(0.1)
                    continue

                self._enqueue_event.clear()

                coros = []
                data = {
                    element_id: None if element is None else element._to_dict()  # pylint: disable=protected-access
                    for element_id, element in self.updates.items()
                }
                coros.append(self._emit('update', data, self.client.id))
                self.updates.clear()

                for target_id, message_type, data in self.messages:
                    coros.append(self._emit(message_type, data, target_id))
                self.messages.clear()

                for coro in coros:
                    try:
                        await coro
                    except Exception as e:
                        core.app.handle_exception(e)

            except Exception as e:
                core.app.handle_exception(e)
                await asyncio.sleep(0.1)

    async def _emit(self, message_type: MessageType, data: Any, target_id: ClientId) -> None:
        await core.sio.emit(message_type, data, room=target_id)
        if core.air is not None and core.air.is_air_target(target_id):
            await core.air.emit(message_type, data, room=target_id)

    def stop(self) -> None:
        """Stop the outbox loop."""
        self._should_stop = True
