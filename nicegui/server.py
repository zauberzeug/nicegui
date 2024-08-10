from __future__ import annotations

import multiprocessing
from redis import Redis, RedisCluster
import socket
from typing import List, Optional, Union

import uvicorn

from . import core, storage
from .native import native


class CustomServerConfig(uvicorn.Config):
    storage_secret: Optional[str] = None
    method_queue: Optional[multiprocessing.Queue] = None
    response_queue: Optional[multiprocessing.Queue] = None
    redis_client: Optional[Union[Redis, RedisCluster]] = None
    redis_session_ttl: Optional[int] = None


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
            core.app.native.main_window = native.WindowProxy()
            native.method_queue = self.config.method_queue
            native.response_queue = self.config.response_queue

        storage.set_storage_secret(self.config.storage_secret)
        storage.set_storage_redis_client(self.config.redis_client, ttl=self.config.redis_session_ttl)
        super().run(sockets=sockets)
