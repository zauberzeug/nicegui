import asyncio
from collections import deque
from typing import TYPE_CHECKING, Any, Deque, Literal, Tuple

from . import globals

if TYPE_CHECKING:
    from .element import Element
    ClientId = int
    MessageType = Literal['update', 'run_method', 'run_javascript', 'open', 'notify']
    MessageGroup = Tuple[ClientId, MessageType, Any]

queue: Deque['MessageGroup'] = deque()


def enqueue_update(element: 'Element') -> None:
    if queue:
        client_id, message_type, argument = queue[-1]
        if client_id == element.client.id and message_type == 'update':
            elements: Deque[Element] = argument
            elements.append(element)
            return
    queue.append((element.client.id, 'update', deque([element])))


def enqueue_message(message_type: 'MessageType', data: Any, client_id: 'ClientId') -> None:
    queue.append((client_id, message_type, data))


async def loop() -> None:
    while True:
        while queue:
            client_id, message_type, data = queue.popleft()
            if message_type == 'update':
                messages: Deque[Element] = data
                data = {'elements': {e.id: e.to_dict() for e in messages}}
            await globals.sio.emit(message_type, data, room=client_id)
        await asyncio.sleep(0.01)
