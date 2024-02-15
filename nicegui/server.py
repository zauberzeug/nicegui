from __future__ import annotations

import multiprocessing
import socket
from typing import List, Optional

import uvicorn

from . import core, storage
from .native import native


class CustomServerConfig(uvicorn.Config):
    """
    CustomServerConfig is a subclass of uvicorn.Config that adds additional attributes for storage_secret,
    method_queue, and response_queue.

    Attributes:
        storage_secret (Optional[str]): The secret used for storage.
        method_queue (Optional[multiprocessing.Queue]): The queue used for method communication.
        response_queue (Optional[multiprocessing.Queue]): The queue used for response communication.
    """

    storage_secret: Optional[str] = None
    method_queue: Optional[multiprocessing.Queue] = None
    response_queue: Optional[multiprocessing.Queue] = None


class Server(uvicorn.Server):
    instance: Server

    @classmethod
    def create_singleton(cls, config: CustomServerConfig) -> None:
        """Create a singleton instance of the server.

        Args:
            config (CustomServerConfig): The configuration for the server.

        Returns:
            None
        """
        cls.instance = cls(config=config)

    def run(self, sockets: Optional[List[socket.socket]] = None) -> None:
        """Run the server.

        This method runs the server and sets up the necessary configurations
        for communication between the server and the client.

        Args:
            sockets (Optional[List[socket.socket]]): A list of sockets to use for
                the server. If not provided, the default sockets will be used.

        Returns:
            None
        """
        self.instance = self
        assert isinstance(self.config, CustomServerConfig)
        if self.config.method_queue is not None and self.config.response_queue is not None:
            core.app.native.main_window = native.WindowProxy()
            native.method_queue = self.config.method_queue
            native.response_queue = self.config.response_queue

        storage.set_storage_secret(self.config.storage_secret)
        super().run(sockets=sockets)
