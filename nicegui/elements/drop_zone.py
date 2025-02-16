from .. import core
from ..element import Element
from ..events import GenericEventArguments


class DropZone(Element, component="drop_zone.js"):
    def __init__(self):
        super().__init__()

        self.on("__file-dropped", handler=self.file_dropped_handler)

        if hasattr(core.app, "native"):
            from nicegui.native.native_mode import drop_events

            drop_events.subscribe(self._handle_native_drop)

    def _handle_native_drop(self, files):
        print("_handle_native_drop")
        print(files)

    def file_dropped_handler(self, event: GenericEventArguments):
        print("file_dropped_handler")
        print(event)
