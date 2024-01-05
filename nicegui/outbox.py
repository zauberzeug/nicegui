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
        if core.app.is_started:
            background_tasks.create(self.loop(), name=f'outbox loop {client.id}')
        else:
            core.app.on_startup(self.loop)

    def enqueue_update(self, element: Element) -> None:
        """Enqueue an update for the given element."""
        self.updates[element.id] = element

    def enqueue_delete(self, element: Element) -> None:
        """Enqueue a deletion for the given element."""
        self.updates[element.id] = None

    def enqueue_message(self, message_type: MessageType, data: Any, target_id: ClientId) -> None:
        """Enqueue a message for the given client."""
        self.messages.append((target_id, message_type, data))

    async def loop(self) -> None:
        """Send updates and messages to all clients in an endless loop."""
        while not self._should_stop:
            try:
                await asyncio.sleep(0.01)

                if not self.updates and not self.messages:
                    continue

                if not self.client.has_socket_connection:
                    continue

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
