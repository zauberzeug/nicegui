from __future__ import annotations

import asyncio
import time
from collections import deque
from typing import TYPE_CHECKING, Any, Deque, Dict, Optional, Tuple

from . import background_tasks, core

if TYPE_CHECKING:
    from .client import Client
    from .element import Element

ElementId = int

ClientId = str
MessageType = str
Payload = Any
Message = Tuple[ClientId, MessageType, Payload]

MessageId = int
MessageTime = float
HistoryEntry = Tuple[MessageId, MessageTime, Message]


class Outbox:

    def __init__(self, client: Client) -> None:
        self.client = client
        self.updates: Dict[ElementId, Optional[Element]] = {}
        self.messages: Deque[Message] = deque()
        self.message_history: Deque[HistoryEntry] = deque()
        self.next_message_id: int = 0

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
                if self.updates:
                    data = {
                        element_id: None if element is None else element._to_dict()  # pylint: disable=protected-access
                        for element_id, element in self.updates.items()
                    }
                    coros.append(self._emit((self.client.id, 'update', data)))
                    self.updates.clear()

                if self.messages:
                    for message in self.messages:
                        coros.append(self._emit(message))
                    self.messages.clear()

                for coro in coros:
                    try:
                        await coro
                    except Exception as e:
                        core.app.handle_exception(e)

            except Exception as e:
                core.app.handle_exception(e)
                await asyncio.sleep(0.1)

    async def _emit(self, message: Message) -> None:
        client_id, message_type, data = message
        data['_id'] = self.next_message_id

        await core.sio.emit(message_type, data, room=client_id)
        if core.air is not None and core.air.is_air_target(client_id):
            await core.air.emit(message_type, data, room=client_id)

        if not self.client.shared:
            self.message_history.append((self.next_message_id, time.time(), message))
            max_age = core.sio.eio.ping_interval + core.sio.eio.ping_timeout + self.client.page.resolve_reconnect_timeout()
            while self.message_history and self.message_history[0][1] < time.time() - max_age:
                self.message_history.popleft()
            while len(self.message_history) > core.app.config.message_history_length:
                self.message_history.popleft()

        self.next_message_id += 1

    def try_rewind(self, target_message_id: MessageId) -> None:
        """Rewind to the given message ID and discard all messages before it."""
        # nothing to do, the next message ID is already the target message ID
        if self.next_message_id == target_message_id:
            return

        # rewind to the target message ID
        while self.message_history:
            self.next_message_id, _, message = self.message_history.pop()
            self.messages.appendleft(message)
            if self.next_message_id == target_message_id:
                self.message_history.clear()
                self._set_enqueue_event()
                return

        # target message ID not found, reload the page
        if not self.client.shared:
            self.client.run_javascript('window.location.reload()')

    def prune_history(self, next_message_id: MessageId) -> None:
        """Prune the message history up to the given message ID."""
        while self.message_history and self.message_history[0][0] < next_message_id:
            self.message_history.popleft()

    def stop(self) -> None:
        """Stop the outbox loop."""
        self._should_stop = True
