from __future__ import annotations

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, DefaultDict, Deque, Dict, List, Optional, Tuple

from . import core
from .dataclasses import KWONLY_SLOTS

if TYPE_CHECKING:
    from .air import Air
    from .client import Client
    from .element import Element


@dataclass(**KWONLY_SLOTS)
class DelayedUpdate:
    time: float = 0
    data: Dict[ElementId, Optional[Dict]] = field(default_factory=dict)


@dataclass(**KWONLY_SLOTS)
class DelayedMessage:
    time: float
    target_id: str
    message_type: str
    data: Any


ClientId = str
ElementId = int
MessageType = str
Message = Tuple[ClientId, MessageType, Any]

waiting_updates: DefaultDict[ClientId, Dict[ElementId, Optional[Element]]] = defaultdict(dict)
delayed_updates: DefaultDict[ClientId, DelayedUpdate] = defaultdict(DelayedUpdate)
waiting_messages: Deque[Message] = deque()
delayed_messages: List[DelayedMessage] = []


def enqueue_update(element: Element) -> None:
    """Enqueue an update for the given element."""
    waiting_updates[element.client.id][element.id] = element


def enqueue_delete(element: Element) -> None:
    """Enqueue a deletion for the given element."""
    waiting_updates[element.client.id][element.id] = None


def enqueue_message(message_type: MessageType, data: Any, target_id: ClientId) -> None:
    """Enqueue a message for the given client."""
    waiting_messages.append((target_id, message_type, data))


async def loop(air: Optional[Air], clients: Dict[str, Client]) -> None:
    """Emit queued updates and messages in an endless loop."""
    async def emit(message_type: MessageType, data: Any, target_id: ClientId) -> None:
        await core.sio.emit(message_type, data, room=target_id)
        if air is not None and air.is_air_target(target_id):
            await air.emit(message_type, data, room=target_id)

    while True:
        await asyncio.sleep(0.01)

        if not delayed_updates and not waiting_updates and not delayed_messages and not waiting_messages:
            continue

        coros = []
        try:
            # process delayed_updates
            for client_id in list(delayed_updates):
                update = delayed_updates[client_id]
                client = clients.get(client_id)
                if client is None or client.has_socket_connection:
                    coros.append(emit('update', update.data, client_id))
                    delayed_updates.pop(client_id)
                elif time.time() > update.time + 3.0:
                    delayed_updates.pop(client_id)

            # process waiting_updates
            for client_id, elements in waiting_updates.items():
                data = {
                    element_id: None if element is None else element._to_dict()  # pylint: disable=protected-access
                    for element_id, element in elements.items()
                }
                client = clients.get(client_id)
                if client is None or client.has_socket_connection:
                    coros.append(emit('update', data, client_id))
                else:
                    delayed_updates[client_id].time = time.time()
                    delayed_updates[client_id].data.update(data)
            waiting_updates.clear()

            # process delayed_messages
            for i, message in enumerate(list(delayed_messages)):
                client = clients.get(message.target_id)
                if client is None or client.has_socket_connection:
                    coros.append(emit(message.message_type, message.data, message.target_id))
                    delayed_messages.pop(i)
                elif time.time() > message.time + 3.0:
                    delayed_messages.pop(i)

            # process waiting_messages
            for target_id, message_type, data in waiting_messages:
                client = clients.get(target_id)
                if client is None or client.has_socket_connection:
                    coros.append(emit(message_type, data, target_id))
                else:
                    message = DelayedMessage(time=time.time(),
                                             target_id=target_id, message_type=message_type, data=data)
                    delayed_messages.append(message)
            waiting_messages.clear()

            # run coroutines
            for coro in coros:
                try:
                    await coro
                except Exception as e:
                    core.app.handle_exception(e)
        except Exception as e:
            core.app.handle_exception(e)
            await asyncio.sleep(0.1)
