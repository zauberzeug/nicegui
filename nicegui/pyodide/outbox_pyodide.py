"""Pyodide-specific outbox with microtask-based auto-flush."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from .. import background_tasks, core
from ..dependencies import JsComponent
from ..outbox import Deleted, Outbox, deleted

if TYPE_CHECKING:
    from ..client import Client

ELEMENTS_DIR = Path(__file__).parent.parent / 'elements'


class PyodideOutbox(Outbox):
    """Outbox for Pyodide mode with microtask-based auto-flush.

    Instead of a continuous background loop, a one-shot flush task is scheduled
    whenever updates or messages are enqueued.  This ensures that out-of-band
    changes (background tasks, timers, ``await run_javascript``) reach the
    JavaScript frontend without an explicit ``flush()`` call.
    """

    def __init__(self, client: Client) -> None:
        import weakref  # pylint: disable=import-outside-toplevel
        from collections import deque  # pylint: disable=import-outside-toplevel

        self._client = weakref.ref(client)
        self.updates: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self.messages: deque = deque()
        self.message_history: deque = deque()
        self.next_message_id: int = 0
        self._loaded_components: set[str] = set()
        self._should_stop = False
        self._enqueue_event = None
        self._flush_pending = False

    def _set_enqueue_event(self) -> None:
        """Schedule an automatic flush on the next event loop iteration.

        All synchronous enqueues within the same execution frame share a single
        flush task, which runs once the current code yields (e.g. ``await``).
        """
        if self._flush_pending or core.loop is None:
            return
        self._flush_pending = True
        background_tasks.create(self._auto_flush(), name='pyodide auto-flush')

    async def _auto_flush(self) -> None:
        """Flush pending updates and messages, then allow new flushes to be scheduled."""
        self._flush_pending = False
        await self.flush()

    async def flush(self) -> None:
        """Flush all pending updates and messages to the JavaScript frontend."""
        client = self._client()
        if client is None:
            return

        coros = []
        if self.updates:
            data = {
                element_id: None if element is deleted
                else element._to_dict()  # type: ignore  # pylint: disable=protected-access
                for element_id, element in self.updates.items()
            }
            js_components = [
                component
                for element in self.updates.values()
                if not isinstance(element, Deleted)
                and isinstance((component := element.component), JsComponent)
                and component.name not in self._loaded_components
            ]
            if js_components:
                comp_list = []
                for c in js_components:
                    try:
                        rel = c.path.relative_to(ELEMENTS_DIR)
                    except ValueError:
                        continue
                    comp_list.append({'url': f'./components/{rel}', 'tag': c.tag})
                if comp_list:
                    coros.append(self._emit((client.id, 'load_js_components', {
                        'components': comp_list,
                    })))
                self._loaded_components.update(c.name for c in js_components)
            coros.append(self._emit((client.id, 'update', data)))
            self.updates.clear()

        if self.messages:
            for message in self.messages:
                coros.append(self._emit(message))
            self.messages.clear()

        for coro in coros:
            try:
                await coro
            except Exception as e:
                core.app.handle_exception(e)
