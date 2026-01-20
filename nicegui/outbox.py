from __future__ import annotations

import asyncio
import time
import weakref
from collections import deque
from typing import TYPE_CHECKING, Any

from . import background_tasks, core
from .dependencies import JsComponent

if TYPE_CHECKING:
    from .client import Client
    from .element import Element

ElementId = int

ClientId = str
MessageType = str
Payload = Any
Message = tuple[ClientId, MessageType, Payload]

MessageId = int
MessageTime = float
HistoryEntry = tuple[MessageId, MessageTime, Message]


class Deleted:
    """Class for creating a sentinel value for deleted elements."""


deleted = Deleted()


class Outbox:

    def __init__(self, client: Client) -> None:
        self._client = weakref.ref(client)
        self.updates: weakref.WeakValueDictionary[ElementId, Element | Deleted] = weakref.WeakValueDictionary()
        self.messages: deque[Message] = deque()
        self.message_history: deque[HistoryEntry] = deque()
        self.next_message_id: int = 0

        self._loaded_components: set[str] = set()
        self._should_stop = False
        self._enqueue_event: asyncio.Event | None = None

        if core.app.is_started:
            background_tasks.create(self.loop(), name=f'outbox loop {client.id}')
        else:
            core.app.on_startup(self.loop)

    @property
    def client(self) -> Client:
        """The client this outbox belongs to."""
        client = self._client()
        if client is None:
            raise RuntimeError('The client this outbox belongs to has been deleted.')
        return client

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
        self.updates[element.id] = deleted
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

                client = self.client
                if not client or not client.has_socket_connection:
                    await asyncio.sleep(0.1)
                    continue

                self._enqueue_event.clear()

                coros = []
                if self.updates:
                    data = {
                        element_id: None if element is deleted else element._to_dict()  # type: ignore  # pylint: disable=protected-access
                        for element_id, element in self.updates.items()
                    }
                    js_components = [
                        component
                        for element in self.updates.values()
                        if not isinstance(element, Deleted)
                        and isinstance((component := element.component), JsComponent)
                        and component.name not in self._loaded_components
                    ]
                    if js_components:
                        coros.append(self._emit((client.id, 'load_js_components', {
                            'components': [{'key': c.key, 'tag': c.tag} for c in js_components],
                        })))
                        self._loaded_components.update(c.name for c in js_components)
                    coros.append(self._emit((client.id, 'update', data)))
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
            except asyncio.CancelledError:
                break
            except Exception as e:
                core.app.handle_exception(e)
                await asyncio.sleep(0.1)

    async def _emit(self, message: Message) -> None:
        client_id, message_type, data = message
        data['_id'] = self.next_message_id

        await core.sio.emit(message_type, data, room=client_id)
        if core.air is not None and core.air.is_air_target(client_id):
            await core.air.emit(message_type, data, room=client_id)

        client = self.client
        if client:
            self.message_history.append((self.next_message_id, time.time(), message))
            max_age = core.sio.eio.ping_interval + core.sio.eio.ping_timeout + client.page.resolve_reconnect_timeout()
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
        self.client.run_javascript('window.location.reload()')

    def prune_history(self, next_message_id: MessageId) -> None:
        """Prune the message history up to the given message ID."""
        while self.message_history and self.message_history[0][0] < next_message_id:
            self.message_history.popleft()

    def stop(self) -> None:
        """Stop the outbox loop."""
        self._should_stop = True
