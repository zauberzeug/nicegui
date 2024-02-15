from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional

from typing_extensions import Self

from .logging import log

if TYPE_CHECKING:
    from .element import Element


class Slot:
    """
    Represents a slot in NiceGUI, which is used to manage the current slot in each asyncio task.

    Attributes:
        stacks (Dict[int, List[Slot]]): A dictionary that maps asyncio task IDs to slot stacks.
            Each slot stack keeps track of the current slot in each task.
        name (str): The name of the slot.
        parent (Element): The parent element of the slot.
        template (Optional[str]): The template associated with the slot.
        children (List[Element]): The list of child elements of the slot.

    Usage:
        A Slot object is used as a context manager using the `with` statement.
        When entering the context, the slot is added to the slot stack of the current asyncio task.
        When exiting the context, the slot is removed from the slot stack and the stack is pruned if empty.
    """

    stacks: Dict[int, List[Slot]] = {}
    

    def __init__(self, parent: Element, name: str, template: Optional[str] = None) -> None:
        """
        Initializes a Slot object.

        Args:
            parent (Element): The parent element of the slot.
            name (str): The name of the slot.
            template (Optional[str]): The template associated with the slot.

        """
        self.name = name
        self.parent = parent
        self.template = template
        self.children: List[Element] = []

    def __enter__(self) -> 'Slot':
        """
        Enters the context of the slot.

        Returns:
            Slot: The current Slot object.

        """
        self.get_stack().append(self)
        return self

    def __exit__(self, *_) -> None:
        """
        Exits the context of the slot.

        """
        self.get_stack().pop()
        self.prune_stack()

    def __iter__(self) -> Iterator[Element]:
        """
        Returns an iterator over the children elements of the slot.

        Returns:
            Iterator[Element]: An iterator over the children elements.

        """
        return iter(self.children)

    @classmethod
    def get_stack(cls) -> List['Slot']:
        """
        Returns the slot stack of the current asyncio task.

        Returns:
            List[Slot]: The slot stack of the current asyncio task.

        """
        task_id = get_task_id()
        if task_id not in cls.stacks:
            cls.stacks[task_id] = []
        return cls.stacks[task_id]

    @classmethod
    def prune_stack(cls) -> None:
        """
        Removes the current slot stack if it is empty.

        """
        task_id = get_task_id()
        if not cls.stacks[task_id]:
            del cls.stacks[task_id]

    @classmethod
    async def prune_stacks(cls) -> None:
        """
        Removes stale slot stacks in an endless loop.

        This method is intended to be run in a separate asyncio task.

        """
        while True:
            try:
                running = [id(task) for task in asyncio.tasks.all_tasks() if not task.done() and not task.cancelled()]
                stale_ids = [task_id for task_id in cls.stacks if task_id not in running]
                for task_id in stale_ids:
                    del cls.stacks[task_id]
            except Exception:
                # NOTE: make sure the loop doesn't crash
                log.exception('Error while pruning slot stacks')
            await asyncio.sleep(10)


def get_task_id() -> int:
    """Return the ID of the current asyncio task.

    This function returns the ID of the current asyncio task. If there is no
    current task, it returns 0.

    Returns:
        int: The ID of the current asyncio task, or 0 if there is no current task.
    """
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0
