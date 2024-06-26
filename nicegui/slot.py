from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, ClassVar, Dict, Iterator, List, Optional

from typing_extensions import Self

from .logging import log

if TYPE_CHECKING:
    from .element import Element


class Slot:
    stacks: ClassVar[Dict[int, List[Slot]]] = {}
    """Maps asyncio task IDs to slot stacks, which keep track of the current slot in each task."""

    def __init__(self, parent: Element, name: str, template: Optional[str] = None) -> None:
        self.name = name
        self.parent = parent
        self.template = template
        self.children: List[Element] = []

    def __enter__(self) -> Self:
        self.get_stack().append(self)
        return self

    def __exit__(self, *_) -> None:
        self.get_stack().pop()
        self.prune_stack()

    def __iter__(self) -> Iterator[Element]:
        return iter(self.children)

    @classmethod
    def get_stack(cls) -> List[Slot]:
        """Return the slot stack of the current asyncio task."""
        task_id = get_task_id()
        if task_id not in cls.stacks:
            cls.stacks[task_id] = []
        return cls.stacks[task_id]

    @classmethod
    def prune_stack(cls) -> None:
        """Remove the current slot stack if it is empty."""
        task_id = get_task_id()
        if not cls.stacks[task_id]:
            del cls.stacks[task_id]

    @classmethod
    async def prune_stacks(cls) -> None:
        """Remove stale slot stacks in an endless loop."""
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
    """Return the ID of the current asyncio task."""
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0
