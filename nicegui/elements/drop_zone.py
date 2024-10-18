from queue import Empty, Queue
from threading import Event, Thread
from typing import Any

from .. import core, native
from ..element import Element
from ..events import GenericEventArguments
from ..server import Server


class DropZone(Element, component="drop_zone.js"):
    def __init__(self):
        super().__init__()

        self.drop_info = Queue()
        self.stop_thread = Event()
        self.thread = Thread(target=self.wait_for_file_info, args=(self.drop_info,), name=f"drop_zone_{self.id}")
        self.thread.start()
        self.on("__file-dropped", handler=self.file_dropped_handler)

    def wait_for_file_info(self, drop_info: Queue[Any]):
        while True:
            try:
                data = native.drop_queue.get(timeout=0.1)
                if data:
                    drop_info.put(data)
            except Empty:
                if core.app.is_stopped or core.app.is_stopping or Server.instance.should_exit:
                    return

    def file_dropped_handler(self, event: GenericEventArguments):
        data = self.drop_info.get()
        self.run_method("drop_emitter", data)
