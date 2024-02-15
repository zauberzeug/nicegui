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
    """
    The Outbox class is responsible for managing updates and messages to be sent to clients in an endless loop.

    Args:
        client (Client): The client associated with the outbox.

    Attributes:
        client (Client): The client associated with the outbox.
        updates (Dict[ElementId, Optional[Element]]): A dictionary that stores the updates to be sent to clients.
        messages (Deque[Message]): A deque that stores the messages to be sent to clients.
        _should_stop (bool): A flag indicating whether the outbox loop should stop.

    Methods:
        enqueue_update(element: Element) -> None:
            Enqueues an update for the given element.
        enqueue_delete(element: Element) -> None:
            Enqueues a deletion for the given element.
        enqueue_message(message_type: MessageType, data: Any, target_id: ClientId) -> None:
            Enqueues a message for the given client.
        loop() -> None:
            Sends updates and messages to all clients in an endless loop.
        _emit(message_type: MessageType, data: Any, target_id: ClientId) -> None:
            Emits a message to the specified client.
        stop() -> None:
            Stops the outbox loop.
    """

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
        """
        Enqueues an update for the given element.

        Args:
            element (Element): The element to be updated.
        """
        self.updates[element.id] = element

    def enqueue_delete(self, element: Element) -> None:
        """
        Enqueues a deletion for the given element.

        Args:
            element (Element): The element to be deleted.
        """
        self.updates[element.id] = None

    def enqueue_message(self, message_type: MessageType, data: Any, target_id: ClientId) -> None:
        """
        Enqueues a message for the given client.

        Args:
            message_type (MessageType): The type of the message.
            data (Any): The data to be sent in the message.
            target_id (ClientId): The ID of the target client.
        """
        self.messages.append((target_id, message_type, data))

    async def loop(self) -> None:
        """
        Sends updates and messages to all clients in an endless loop.
        """
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
        """
        Emits a message to the specified client.

        Args:
            message_type (MessageType): The type of the message.
            data (Any): The data to be sent in the message.
            target_id (ClientId): The ID of the target client.
        """
        await core.sio.emit(message_type, data, room=target_id)
        if core.air is not None and core.air.is_air_target(target_id):
            await core.air.emit(message_type, data, room=target_id)

    def stop(self) -> None:
        """
        Stops the outbox loop.
        """
        self._should_stop = True
