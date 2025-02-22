import asyncio
import queue
from typing import Optional

from typing_extensions import Self

from .. import core, ui
from ..element import Element
from ..events import GenericEventArguments
from ..native import drop_queue


class DropZone(Element, component='drop_zone.js'):
    def __init__(
        self,
        drop_style: str | None = None,
        cleared_drop_style: str = '',
    ):
        super().__init__()

        self.default_classes('relative')
        self.classes('relative')

        self.drop_style = drop_style
        if self.drop_style is None:
            self.drop_style = 'absolute inset-0 m-1 border-2 border-dashed border-neutral-700 pointer-events-none'
        self.cleared_drop_style = cleared_drop_style
        self._clear_drop_style()

        self.on('drag_over', handler=self._set_hover_style)
        self.on('drag_leave', handler=self._clear_hover_style)
        self.on('__file-dropped', handler=self.file_dropped_handler)
        self.check_task: Optional[asyncio.Task] = None

    def file_dropped_handler(self, event: GenericEventArguments):
        if core.app.config.reload:
            ui.notify('Drop zones does not work when auto-reloading is on')
        if self.check_task is None or self.check_task.done():
            self.check_task = asyncio.create_task(self.check_queue_loop())

    async def check_queue_loop(self):
        timeout_count = 0
        while timeout_count < 10:  # Stop checking after 1 second of no activity
            try:
                while not drop_queue.empty():
                    data = drop_queue.get_nowait()
                    self.run_method('drop_emitter', data)
                    return
                timeout_count += 1
            except queue.Empty:
                timeout_count += 1
            await asyncio.sleep(0.1)

        return self

    def update_hover_style(self, hover_style: str) -> Self:
        self.hover_style = hover_style
        return self
    def _set_hover_style(self):
        self._props['hover_style'] = self.hover_style
        self.update()

    def _clear_hover_style(self):
        self._props['hover_style'] = self.cleared_hover_style
        self.update()
