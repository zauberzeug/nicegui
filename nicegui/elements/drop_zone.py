import asyncio
import queue
from typing import ClassVar, List, Optional, cast

from typing_extensions import Self

from .. import core, ui
from ..classes import Classes
from ..element import Element
from ..events import DropZoneEventArguments, GenericEventArguments, Handler, KeyboardModifiers, handle_event
from ..native import drop_queue


class DropZone(Element, component='drop_zone.js'):

    _default_hover_classes: ClassVar[List[str]] = []
    _default_hover_overlay_classes: ClassVar[List[str]] = []

    def __init__(
        self,
        on_drop: Optional[Handler[DropZoneEventArguments]] = None,
    ) -> None:
        """Drop Zone

        Uses PyWebview's `Drag Drop <https://pywebview.flowrl.com/examples/drag_drop.html>`_ functionality.
        This element will return the path to the file or folder that got dropped into it.

        This controller only works in NiceGUI native mode.

        :param on_drop:	callback to execute for each dropped object
        """
        super().__init__()

        self._hover_classes: Classes[Self] = Classes(self._default_hover_classes, element=cast(Self, self))
        self._hover_overlay_classes: Classes[Self] = Classes(
            self._default_hover_overlay_classes, element=cast(Self, self))

        self._drop_handlers = [on_drop] if on_drop else []

        self.on('drag_over', handler=self._set_hover_style)
        self.on('drag_leave', handler=self._clear_hover_style)
        self.on('__file_dropped', handler=self.file_dropped_handler)
        self.check_task: Optional[asyncio.Task] = None

    @property
    def classes(self) -> Classes[Self]:
        """The classes of the element."""
        return self._classes

    @property
    def hover_classes(self) -> Classes[Self]:
        """The classes of the element."""
        return self._hover_classes

    @property
    def hover_overlay_classes(self) -> Classes[Self]:
        """The classes of the element."""
        return self._hover_overlay_classes

    def file_dropped_handler(self, event: GenericEventArguments):
        if core.app.config.reload:
            ui.notify('Drop zones does not work when auto-reloading is enabled')
        if self.check_task is None or self.check_task.done():
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
        self.props['hover_overlay_style'] = self._get_class_string(self.hover_overlay_classes)
        self.classes(add=self._get_class_string(self.hover_classes))
        self.update()

    def _clear_hover_style(self):
        self.props['hover_overlay_style'] = ''
        self.classes(remove=self._get_class_string(self.hover_classes))
        self.update()

    def _get_class_string(self, classes: list[str]) -> str:
        return ' '.join(classes)
