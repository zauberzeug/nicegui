import asyncio
from typing import TYPE_CHECKING, Dict, List, Set

from . import globals

if TYPE_CHECKING:
    from .element import Element

update_queue: Dict[int, List] = {}  # element id -> [element, attributes]


def enqueue(element: 'Element', *attributes: str) -> None:
    '''Schedules a UI update for this element.

    Attributes can be 'class', 'style', 'props', or 'text'.
    '''
    if element.id not in update_queue:
        update_queue[element.id] = [element, list(attributes)]
    else:
        queued_attributes: Set[str] = update_queue[element.id][1]
        if queued_attributes and attributes:
            queued_attributes.update(attributes)
        else:
            queued_attributes.clear()


async def loop() -> None:
    '''Repeatedly updates all elements in the update queue.'''
    while True:
        elements: Dict[int, 'Element'] = {}
        for id, value in sorted(update_queue.items()):  # NOTE: sort by element ID to process parents before children
            if id in elements:
                continue
            element: 'Element' = value[0]
            for id in element.collect_descendant_ids():
                elements[id] = element.client.elements[id].to_dict()
        if elements:
            await globals.sio.emit('update', {'elements': elements}, room=element.client.id)
            update_queue.clear()
        else:
            await asyncio.sleep(0.01)
