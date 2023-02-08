import asyncio
from collections import deque
from typing import TYPE_CHECKING, Any, Deque, Dict, Set, Tuple

from . import globals

if TYPE_CHECKING:
    from .element import Element
    ClientId = int
    MessageType = str
    MessageGroup = Tuple[ClientId, MessageType, Any]

queue: Deque['MessageGroup'] = deque()


def enqueue_update(element: 'Element', *attributes: str) -> None:
    client_id, message_type, data = queue[-1] if queue else (None, None, None)
    if client_id != element.client.id or message_type != 'update':
        # add new message group
        queue.append((element.client.id, 'update', {element.id: (element, set())}))
        return
    elements: Dict[int, Tuple[Element, Set]] = data
    if element.id not in elements:
        # add new element to message group
        elements[element.id] = [element, set()]
        return
    if attributes:
        # enqueue single attributes
        elements[element.id][1].update(attributes)
    else:
        # enqueue all attributes
        elements[element.id][1].clear()


def enqueue_message(message_type: 'MessageType', data: Any, client_id: 'ClientId') -> None:
    _convert_elements_to_dicts()
    queue.append((client_id, message_type, data))


async def loop() -> None:
    while True:
        while queue:
            _convert_elements_to_dicts()
            client_id, message_type, data = queue.popleft()
            await globals.sio.emit(message_type, data, room=client_id)
        await asyncio.sleep(0.01)


def _convert_elements_to_dicts() -> None:
    _, message_type, data = queue[-1] if queue else (None, None, None)
    if message_type == 'update':
        elements: Dict[int, Tuple[Element, Set]] = data
        for id, value in elements.items():
            if len(value) == 2:
                element, attributes = value
                elements[id] = element.to_dict(*attributes)
