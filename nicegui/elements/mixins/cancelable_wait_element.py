import asyncio
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from ...element import Element


class CancelableWaitElement(Element):
    """Cancel tasks awaiting an interaction with this element when it is deleted.

    Unlike ``Dialog``, which resolves pending awaits with ``None`` on deletion, elements using this mixin
    cancel the awaiting task: their awaits have no "didn't happen" return channel,
    so resuming them would be indistinguishable from the awaited interaction actually occurring.
    """

    def __init__(self, **kwargs: Any) -> None:
        # NOTE: assigned before super().__init__ which registers the element,
        # so _handle_delete finds the dict even if a subclass constructor fails halfway
        self._waiting_tasks: dict[asyncio.Task, asyncio.Event] = {}
        super().__init__(**kwargs)

    @contextmanager
    def _cancel_when_deleted(self, event: asyncio.Event) -> Iterator[None]:
        """Cancel the current task if this element is deleted before ``event`` is set.

        A deleted element can never fire the awaited interaction,
        so the task is cancelled rather than resolved to keep the code after the ``await`` from running.
        """
        if self.is_deleted:
            # raise directly instead of task.cancel() so a caller catching the CancelledError keeps a clean task,
            # just like when the deletion happens during the wait
            raise asyncio.CancelledError
        task = asyncio.current_task()
        assert task is not None
        self._waiting_tasks[task] = event
        try:
            yield
        finally:
            self._waiting_tasks.pop(task, None)

    def _handle_delete(self) -> None:
        for task, event in self._waiting_tasks.items():
            if not task.done() and not event.is_set():  # an interaction that was already processed wins over the deletion
                task.cancel()
        self._waiting_tasks.clear()
        super()._handle_delete()
