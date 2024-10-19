from __future__ import annotations

import asyncio
import itertools
import time
from collections import deque
from typing import TYPE_CHECKING, Any, Deque, Dict, Optional, Tuple

from . import background_tasks, core

if TYPE_CHECKING:
    from .client import Client
    from .element import Element

ElementId = int
ClientId = str
MessageId = int
MessageType = str
MessageTime = float
Payload = Any
Message = Tuple[ClientId, MessageId, MessageTime, MessageType, Payload]


class Outbox:

    def __init__(self, client: Client) -> None:
        self.client = client
        self.updates: Dict[ElementId, Optional[Element]] = {}
        self.messages: Deque[Message] = deque()
        self._should_stop = False
        self._enqueue_event: Optional[asyncio.Event] = None
        self.next_message_id: int = 0
        self._message_index: int = 0

        if core.app.is_started:
            background_tasks.create(self.loop(), name=f'outbox loop {client.id}')
        else:
            core.app.on_startup(self.loop)

    @property
    def history_duration(self) -> float:
        """Duration of the message history in seconds."""
        if self.client.shared:
            return 0
        else:
            return core.sio.eio.ping_interval + core.sio.eio.ping_timeout + self.client.page.resolve_reconnect_timeout()

    def _set_enqueue_event(self) -> None:
        """Set the enqueue event while accounting for lazy initialization."""
        if self._enqueue_event:
            self._enqueue_event.set()

    def enqueue_update(self, element: Element) -> None:
        """Enqueue an update for the given element."""
        self.client.check_existence()
        self.updates[element.id] = element
        self._set_enqueue_event()

    def enqueue_delete(self, element: Element) -> None:
        """Enqueue a deletion for the given element."""
        self.client.check_existence()
        self.updates[element.id] = None
        self._set_enqueue_event()

    def enqueue_message(self, message_type: MessageType, data: Payload, target_id: ClientId) -> None:
        """Enqueue a message for the given client."""
        self.client.check_existence()
        self.messages.append((target_id, self.next_message_id, time.time(), message_type, data))
        self.next_message_id += 1
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
                if self.updates:
                    data = {
                        element_id: None if element is None else element._to_dict()  # pylint: disable=protected-access
                        for element_id, element in self.updates.items()
                    }
                    self.messages.append((self.client.id, self.next_message_id, time.time(), 'update', data))
                    self.next_message_id += 1
                    self.updates.clear()

                if len(self.messages) > self._message_index:
                    for message in itertools.islice(self.messages, self._message_index, None):
                        coros.append(self._emit(message))
                    self._prune_messages()
                    self._message_index = len(self.messages)

                for coro in coros:
                    try:
                        await coro
                    except Exception as e:
                        core.app.handle_exception(e)

            except Exception as e:
                core.app.handle_exception(e)
                await asyncio.sleep(0.1)

    async def _emit(self, message: Message) -> None:
        client_id, message_id, _, message_type, data = message
        data['_id'] = message_id
        await core.sio.emit(message_type, data, room=client_id)
        if core.air is not None and core.air.is_air_target(client_id):
            await core.air.emit(message_type, data, room=client_id)

    def _prune_messages(self) -> None:
        if self.client.shared:
            self.messages.clear()
        else:
            while self.messages and self.messages[0][2] < time.time() - self.history_duration:
                self.messages.popleft()

    def seek(self, message_id: MessageId) -> None:
        """Seek to the given message ID and discard all messages before it."""
        while self.messages and self.messages[0][1] < message_id:
            self.messages.popleft()
        self._message_index = 0
        self._set_enqueue_event()

    def stop(self) -> None:
        """Stop the outbox loop."""
        self._should_stop = True
