import asyncio
import time
from typing import ClassVar, List, Optional, cast

from typing_extensions import Self

from .. import background_tasks, core
from ..classes import Classes
from ..element import Element
from ..events import DropZoneEventArguments, GenericEventArguments, Handler, KeyboardModifiers, handle_event
from ..functions.notify import notify
from ..native import native


class DropZone(Element, component='drop_zone.js'):
    _default_hover_classes: ClassVar[List[str]] = []
    _default_hover_overlay_classes: ClassVar[List[str]] = []

    def __init__(self, on_drop: Optional[Handler[DropZoneEventArguments]] = None) -> None:
        """Drop Zone

        Uses PyWebview's `Drag Drop <https://pywebview.flowrl.com/examples/drag_drop.html>`_ functionality.
        This element will return the path to the file or folder that got dropped into it.

        This controller only works in NiceGUI native mode.

        :param on_drop:	callback to execute for each dropped object
        """
        super().__init__()

        self._hover_classes = Classes(self._default_hover_classes, element=cast(Self, self))
        self._hover_overlay_classes = Classes(self._default_hover_overlay_classes, element=cast(Self, self))

        self._drop_handlers = [on_drop] if on_drop else []

        self.on('drag_enter', handler=self._set_hover_style)
        self.on('drag_leave', handler=self._clear_hover_style)
        self.on('file_drop', handler=self._handle_file_drop)
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

    def _handle_file_drop(self, event: GenericEventArguments) -> None:
        if core.app.config.reload:
            notify('Drop zones does not work when auto-reloading is enabled')
        if self.check_task is None or self.check_task.done():
            self.check_task = background_tasks.create(self._check_queue_loop(event))
        self._clear_hover_style()

    async def _check_queue_loop(self, event: GenericEventArguments) -> None:
        deadline = time.time() + 1.0
        while time.time() < deadline:
            if not native.drop_queue.empty():
                args = DropZoneEventArguments(
                    sender=self,
                    client=self.client,
                    path=native.drop_queue.get_nowait(),
                    modifiers=KeyboardModifiers(
                        alt=event.args['altKey'],
                        ctrl=event.args['ctrlKey'],
                        meta=event.args['metaKey'],
                        shift=event.args['shiftKey'],
                    ),
                )
                for drop_handler in self._drop_handlers:
                    handle_event(drop_handler, args)
            await asyncio.sleep(0.1)

    def on_drop(self, callback: Handler[DropZoneEventArguments]) -> Self:
        """Add a callback to be invoked when a file is dropped."""
        self._drop_handlers.append(callback)
        return self

    def _set_hover_style(self) -> None:
        self.props['hover_overlay_style'] = self._get_class_string(self.hover_overlay_classes)
        self.classes(add=self._get_class_string(self.hover_classes))
        self.update()

    def _clear_hover_style(self) -> None:
        self.props['hover_overlay_style'] = ''
        self.classes(remove=self._get_class_string(self.hover_classes))
        self.update()

    def _get_class_string(self, classes: List[str]) -> str:
        return ' '.join(classes)
