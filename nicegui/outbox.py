import asyncio
from collections import defaultdict, deque
from typing import TYPE_CHECKING, Any, DefaultDict, Deque, Dict, Tuple

from . import globals

if TYPE_CHECKING:
    from .element import Element

ClientId = str
ElementId = int
MessageType = str
Message = Tuple[ClientId, MessageType, Any]

update_queue: DefaultDict[ClientId, Dict[ElementId, 'Element']] = defaultdict(dict)
message_queue: Deque[Message] = deque()


def enqueue_update(element: 'Element') -> None:
    update_queue[element.client.id][element.id] = element


def enqueue_delete(element: 'Element') -> None:
    update_queue[element.client.id][element.id] = None


def enqueue_message(message_type: MessageType, data: Any, target_id: ClientId) -> None:
    message_queue.append((target_id, message_type, data))


async def _emit(message_type: MessageType, data: Any, target_id: ClientId) -> None:
    await globals.sio.emit(message_type, data, room=target_id)
    if is_target_on_air(target_id):
        await globals.air.emit(message_type, data, room=target_id)


async def loop() -> None:
    while True:
        if not update_queue and not message_queue:
            await asyncio.sleep(0.01)
            continue

        coros = []
        try:
            for client_id, elements in update_queue.items():
                data = {
                    element_id: element._to_dict() if element else None
                    for element_id, element in elements.items()
                }
                coros.append(_emit('update', data, client_id))
            update_queue.clear()

            for target_id, message_type, data in message_queue:
                coros.append(_emit(message_type, data, target_id))
            message_queue.clear()

            for coro in coros:
                try:
                    await coro
                except Exception as e:
                    globals.handle_exception(e)
        except Exception as e:
            globals.handle_exception(e)
            await asyncio.sleep(0.1)


def is_target_on_air(target_id: str) -> bool:
    if target_id in globals.clients:
        return globals.clients[target_id].on_air
    else:
        return target_id in globals.sio.manager.rooms
