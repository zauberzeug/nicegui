from __future__ import annotations

import asyncio
import time
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
        self._history: Deque[Tuple[int, float, Tuple[MessageType, Any, ClientId]]] = deque()
        self._message_count: int = 0

        if self.client.shared:
            self._history_duration = 30
        else:
            self._history_duration = max(core.sio.eio.ping_interval + core.sio.eio.ping_timeout +
                                         self.client.page.resolve_reconnect_timeout(), 30)

        if core.app.is_started:
            background_tasks.create(self.loop(), name=f'outbox loop {client.id}')
        else:
            core.app.on_startup(self.loop)

    @property
    def message_count(self):
        """Get the total number of messages sent."""
        return self._message_count

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

    def enqueue_message(self, message_type: MessageType, data: Any, target_id: ClientId) -> None:
        """Enqueue a message for the given client."""
        self.client.check_existence()
        self.messages.append((target_id, message_type, data))
        self._set_enqueue_event()

    def _append_history(self, message_type: MessageType, data: Any, target: ClientId) -> int:
        self._message_count += 1
        current_ts = time.time()

        while len(self._history) > 0:
            oldest_ts = self._history[0][1]
            if current_ts - oldest_ts > self._history_duration:
                self._history.popleft()
            else:
                break

        self._history.append((self._message_count, current_ts, (message_type, data, target)))

        return self._message_count

    def synchronize(self, last_msg_id: int) -> bool:
        """Synchronize the state of a reconnecting client by resending missed messages, if possible."""
        if len(self._history) > 0:
            next_id = last_msg_id + 1
            oldest_id = self._history[0][0]
            if oldest_id > next_id:
                return False

            start = next_id - oldest_id
            for i in range(start, len(self._history)):
                self.enqueue_message('retransmit', self._history[i][2], '')
        else:
            if last_msg_id != self._message_count:
                return False

        return True

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
                    coros.append(self._emit('update', data, self.client.id))
                    self.updates.clear()

                if self.messages:
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
        if message_type != 'retransmit':
            data['message_id'] = self._append_history(message_type, data, target_id)
        else:
            message_type, data, target_id = data

        await core.sio.emit(message_type, data, room=target_id)
        if core.air is not None and core.air.is_air_target(target_id):
            await core.air.emit(message_type, data, room=target_id)

    def stop(self) -> None:
        """Stop the outbox loop."""
        self._should_stop = True
