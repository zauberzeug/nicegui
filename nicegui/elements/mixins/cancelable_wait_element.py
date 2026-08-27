import asyncio
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from ...element import Element


class CancelableWaitElement(Element):

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
        task = asyncio.current_task()
        assert task is not None
        if self.is_deleted:
            task.cancel()  # keep the cancellation pending so it is re-delivered even if the caller catches the raise
            raise asyncio.CancelledError
        self._waiting_tasks[task] = event
        try:
            yield
        finally:
            self._waiting_tasks.pop(task, None)

    def _handle_delete(self) -> None:
        for task, event in self._waiting_tasks.items():
            if not task.done() and not event.is_set():  # an interaction that already happened wins over the deletion
                task.cancel()
        self._waiting_tasks.clear()
        super()._handle_delete()
