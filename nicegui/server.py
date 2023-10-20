from __future__ import annotations

import multiprocessing
import socket
from typing import List, Optional

import uvicorn

from . import globals  # pylint: disable=redefined-builtin
from . import storage  # pylint: disable=redefined-builtin
from . import native as native_module


class CustomServerConfig(uvicorn.Config):
    storage_secret: Optional[str] = None
    method_queue: Optional[multiprocessing.Queue] = None
    response_queue: Optional[multiprocessing.Queue] = None


class Server(uvicorn.Server):
    instance: Server

    @classmethod
    def create_singleton(cls, config: CustomServerConfig) -> None:
        """Create a singleton instance of the server."""
        cls.instance = cls(config=config)

    def run(self, sockets: Optional[List[socket.socket]] = None) -> None:
        self.instance = self
        assert isinstance(self.config, CustomServerConfig)
        if self.config.method_queue is not None and self.config.response_queue is not None:
            native_module.method_queue = self.config.method_queue
            native_module.response_queue = self.config.response_queue
            globals.app.native.main_window = native_module.WindowProxy()

        storage.set_storage_secret(self.config.storage_secret)
        super().run(sockets=sockets)
