from queue import Queue
from threading import Thread
from typing import Any

from .. import native
from ..element import Element
from ..events import GenericEventArguments


class DropZone(Element, component="drop_zone.js"):
    def __init__(self):
        super().__init__()

        self.drop_info = Queue()
        Thread(target=self.wait_for_file_info, args=(self.drop_info,), name=f"drop_zone_{self.id}").start()
        self.on("__file-dropped", handler=self.file_dropped_handler)

    def wait_for_file_info(self, drop_info: Queue[Any]):
        while True:
            data = native.drop_queue.get()
            drop_info.put(data)

    def file_dropped_handler(self, event: GenericEventArguments):
        data = self.drop_info.get()
        self.run_method("drop_emitter", data)
