from __future__ import annotations

import multiprocessing
import multiprocessing.synchronize
import socket
import threading
from typing import Any

try:
    import uvicorn
except ImportError:
    uvicorn = None  # type: ignore

from . import core, storage
from .native import native

if uvicorn is not None:
    _ConfigBase = uvicorn.Config
    _ServerBase = uvicorn.Server
else:
    _ConfigBase = object
    _ServerBase = object


class CustomServerConfig(_ConfigBase):
    storage_secret: str | None = None
    method_queue: multiprocessing.Queue | None = None
    response_queue: multiprocessing.Queue | None = None
    shutdown_event: multiprocessing.synchronize.Event | None = None
    session_middleware_kwargs: dict[str, Any] | None = None


class Server(_ServerBase):
    instance: uvicorn.Server

    @classmethod
    def create_singleton(cls, config: CustomServerConfig) -> None:
        """Create a singleton instance of the server."""
        cls.instance = cls(config=config)

    def run(self, sockets: list[socket.socket] | None = None) -> None:
        self.instance = self
        assert isinstance(self.config, CustomServerConfig)
        if self.config.method_queue is not None and self.config.response_queue is not None:
            core.app.native.main_window = native.WindowProxy()
            native.method_queue = self.config.method_queue
            native.response_queue = self.config.response_queue
            if (event := self.config.shutdown_event) is not None:
                def monitor_shutdown_event() -> None:
                    event.wait()
                    self.should_exit = True
                threading.Thread(target=monitor_shutdown_event, daemon=True).start()

        storage.set_storage_secret(self.config.storage_secret, self.config.session_middleware_kwargs)
        super().run(sockets=sockets)
