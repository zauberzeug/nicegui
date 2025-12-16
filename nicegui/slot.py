from __future__ import annotations

import asyncio
import weakref
from collections.abc import Iterator
from typing import TYPE_CHECKING, ClassVar

from typing_extensions import Self

from .logging import log

if TYPE_CHECKING:
    from .element import Element


class Slot:
    stacks: ClassVar[dict[int, list[Slot]]] = {}
    '''Maps asyncio task IDs to slot stacks, which keep track of the current slot in each task.'''

    def __init__(self, parent: Element, name: str, template: str | None = None) -> None:
        self.name = name
        self._parent = weakref.ref(parent)
        self.template = template
        self.children: list[Element] = []

    @property
    def parent(self) -> Element:
        """The parent element this slot belongs to."""
        parent = self._parent()
        if parent is None:
            raise RuntimeError('The parent element this slot belongs to has been deleted.')
        return parent

    def __enter__(self) -> Self:
        self.get_stack().append(self)
        return self

    def __exit__(self, *_) -> None:
        self.get_stack().pop()
        self.prune_stack()

    def __iter__(self) -> Iterator[Element]:
        return iter(self.children)

    @classmethod
    def get_stack(cls) -> list[Slot]:
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
        """Remove stale slot stacks."""
        try:
            running = {id(task) for task in asyncio.tasks.all_tasks() if not task.done() and not task.cancelled()}

            # ID 0 is the special ID used in cases where no task is active (see get_task_id).
            # Since it has no associated task, we always assume it to be active
            # in order to avoid pruning the associated stack while the slot is active.
            running.add(0)

            stale_ids = [task_id for task_id in cls.stacks if task_id not in running]
            for task_id in stale_ids:
                del cls.stacks[task_id]
        except Exception:
            log.exception('Error while pruning slot stacks')


def get_task_id() -> int:
    """Return the ID of the current asyncio task."""
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0
