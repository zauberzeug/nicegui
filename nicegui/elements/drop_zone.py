import asyncio
import queue
from typing import Optional

from typing_extensions import Self

from .. import core, ui
from ..element import Element
from ..events import DropZoneEventArguments, GenericEventArguments, Handler, KeyboardModifiers, handle_event
from ..native import drop_queue


class DropZone(Element, component='drop_zone.js'):

    def __init__(
        self,
        on_drop: Optional[Handler[DropZoneEventArguments]] = None,
        hover_style: str | None = None,
        cleared_hover_style: str = '',
    ) -> None:
        """Drop Zone

        Uses PyWebview's `Drag Drop <https://pywebview.flowrl.com/examples/drag_drop.html>`_ functionality.
        This element will return the path to the file or folder that got dropped into it.

        This controller only works in NiceGUI native mode.

        :param on_drop:	callback to execute for each dropped object
        :param hover_style: change the style that gets applied to the drop zone when an object is hovered
        :param cleared_hover_style: custom style that gets applied after the object have bin dropped
        """
        super().__init__()

        self.default_classes('relative')
        self.classes('relative')

        self.hover_style = hover_style
        if self.hover_style is None:
            self.hover_style = 'absolute inset-0 m-1 border-2 border-dashed border-neutral-700 pointer-events-none'
        self.cleared_hover_style = cleared_hover_style
        self._clear_hover_style()

        self._drop_handlers = [on_drop] if on_drop else []

        self.on('drag_over', handler=self._set_hover_style)
        self.on('drag_leave', handler=self._clear_hover_style)
        self.on('__file-dropped', handler=self.file_dropped_handler)
        self.check_task: Optional[asyncio.Task] = None

    def file_dropped_handler(self, event: GenericEventArguments):
        if core.app.config.reload:
            ui.notify('Drop zones does not work when auto-reloading is enabled')
        if self.check_task is None or self.check_task.done():
            # print("file_dropped_handler", event)
            self.check_task = asyncio.create_task(self.check_queue_loop(event))

    async def check_queue_loop(self, event: GenericEventArguments):
        timeout_count = 0
        while timeout_count < 10:  # Stop checking after 1 second of no activity
            try:
                while not drop_queue.empty():
                    data = drop_queue.get_nowait()
                    event.args['drop'] = data
                    self._handle_drop(event.args)
                    return
                timeout_count += 1
            except queue.Empty:
                timeout_count += 1
            await asyncio.sleep(0.1)

    def on_drop(self, callback: Handler[DropZoneEventArguments]) -> Self:
        """Add a callback to be invoked when a file is dropped."""
        self._drop_handlers.append(callback)
        return self

    def update_hover_style(self, hover_style: str) -> Self:
        self.hover_style = hover_style
        return self

    def _handle_drop(self, event_data) -> None:
        """Handle the uploaded files.

        This method is primarily intended for internal use and for simulating file uploads in tests.
        """
        keyboard_modifiers = KeyboardModifiers(
            alt=event_data['altKey'],
            ctrl=event_data['ctrlKey'],
            meta=event_data['metaKey'],
            shift=event_data['shiftKey'],
        )
        for drop_handler in self._drop_handlers:
            handle_event(drop_handler, DropZoneEventArguments(
                sender=self,
                client=self.client,
                path=event_data['drop'],
                modifiers=keyboard_modifiers,
            ))

    def _set_hover_style(self):
        self._props['hover_style'] = self.hover_style
        self.update()

    def _clear_hover_style(self):
        self._props['hover_style'] = self.cleared_hover_style
        self.update()
