from __future__ import annotations

import multiprocessing
import socket
from typing import Any

import uvicorn

from . import core, storage
from .native import native


class CustomServerConfig(uvicorn.Config):
    storage_secret: str | None = None
    method_queue: multiprocessing.Queue | None = None
    response_queue: multiprocessing.Queue | None = None
    session_middleware_kwargs: dict[str, Any] | None = None


class Server(uvicorn.Server):
    instance: Server

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

        storage.set_storage_secret(self.config.storage_secret, self.config.session_middleware_kwargs)
        super().run(sockets=sockets)
