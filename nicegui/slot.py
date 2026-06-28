from __future__ import annotations

import asyncio
import contextvars
import weakref
from collections.abc import Iterator
from typing import TYPE_CHECKING, ClassVar

from typing_extensions import Self

from .logging import log

if TYPE_CHECKING:
    from .element import Element

# Cache the current task's stack after validating the task ID; ContextVars are copied into new asyncio tasks.
_slot_stack_cache: contextvars.ContextVar[tuple[int, list[Slot] | None] | None] = \
    contextvars.ContextVar('_slot_stack_cache', default=None)


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
        _task_id, stack = self._get_or_create_stack()
        stack.append(self)
        return self

    def __exit__(self, *_) -> None:
        _task_id, stack = self._get_or_create_stack()
        stack.pop()
        # Keep empty stacks cached; prune_stacks removes entries for completed tasks.

    def __iter__(self) -> Iterator[Element]:
        return iter(self.children)

    @classmethod
    def get_stack(cls) -> list[Slot]:
        """Return the slot stack of the current asyncio task."""
        return cls._get_or_create_stack()[1]

    @classmethod
    def peek_stack(cls) -> list[Slot] | None:
        """Return the current task's slot stack without creating one."""
        task_id = get_task_id()
        cached = _slot_stack_cache.get()
        if cached is not None and cached[0] == task_id:
            return cached[1]
        stack = cls.stacks.get(task_id)
        _slot_stack_cache.set((task_id, stack))
        return stack

    @classmethod
    def _get_or_create_stack(cls) -> tuple[int, list[Slot]]:
        """Return (task_id, stack) for the current task."""
        task_id = get_task_id()
        cached = _slot_stack_cache.get()
        if cached is not None and cached[0] == task_id:
            stack = cached[1]
            if stack is not None:
                return task_id, stack
        stack = cls.stacks.get(task_id)
        if stack is None:
            stack = []
            cls.stacks[task_id] = stack
        entry = (task_id, stack)
        _slot_stack_cache.set(entry)
        return entry

    @classmethod
    def prune_stack(cls) -> None:
        """Remove the current slot stack if it is empty."""
        task_id = get_task_id()
        stack = cls.stacks.get(task_id)
        if stack is not None and not stack:
            del cls.stacks[task_id]
            cached = _slot_stack_cache.get()
            if cached is not None and cached[0] == task_id:
                _slot_stack_cache.set(None)

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
