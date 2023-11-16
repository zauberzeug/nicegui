from __future__ import annotations

import asyncio
from collections import defaultdict, deque
from typing import TYPE_CHECKING, Any, DefaultDict, Deque, Dict, Optional, Tuple

from . import core

if TYPE_CHECKING:
    from .air import Air
    from .element import Element

ClientId = str
ElementId = int
MessageType = str
Message = Tuple[ClientId, MessageType, Any]

update_queue: DefaultDict[ClientId, Dict[ElementId, Optional[Element]]] = defaultdict(dict)
message_queue: Deque[Message] = deque()


def enqueue_update(element: Element) -> None:
    """Enqueue an update for the given element."""
    update_queue[element.client.id][element.id] = element


def enqueue_delete(element: Element) -> None:
    """Enqueue a deletion for the given element."""
    update_queue[element.client.id][element.id] = None


def enqueue_message(message_type: MessageType, data: Any, target_id: ClientId) -> None:
    """Enqueue a message for the given client."""
    message_queue.append((target_id, message_type, data))


async def loop(air: Optional[Air]) -> None:
    """Emit queued updates and messages in an endless loop."""
    async def emit(message_type: MessageType, data: Any, target_id: ClientId) -> None:
        await core.sio.emit(message_type, data, room=target_id)
        if air is not None and air.is_air_target(target_id):
            await air.emit(message_type, data, room=target_id)

    while True:
        if not update_queue and not message_queue:
            await asyncio.sleep(0.01)
            continue

        coros = []
        try:
            for client_id, elements in update_queue.items():
                data = {
                    element_id: None if element is None else element._to_dict()  # pylint: disable=protected-access
                    for element_id, element in list(elements.items())
                }
                coros.append(emit('update', data, client_id))
            update_queue.clear()

            for target_id, message_type, data in message_queue:
                coros.append(emit(message_type, data, target_id))
            message_queue.clear()

            for coro in coros:
                try:
                    await coro
                except Exception as e:
                    core.app.handle_exception(e)
        except Exception as e:
            core.app.handle_exception(e)
            await asyncio.sleep(0.1)
