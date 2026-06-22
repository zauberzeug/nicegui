from __future__ import annotations

import asyncio
import multiprocessing
import multiprocessing.synchronize
import os
import socket
import sys
import threading
import time
from contextlib import suppress
from typing import Any

import uvicorn

from . import core, storage
from .native import native


class CustomServerConfig(uvicorn.Config):
    storage_secret: str | None = None
    method_queue: multiprocessing.Queue | None = None
    response_queue: multiprocessing.Queue | None = None
    shutdown_event: multiprocessing.synchronize.Event | None = None
    session_middleware_kwargs: dict[str, Any] | None = None


class Server(uvicorn.Server):
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
                    # Poll instead of `event.wait()`: a blocking wait leaves a stale waiter if the reloader
                    # kills the process mid-wait, making a later `event.set()` hang forever (#5845).
                    while not event.is_set():
                        time.sleep(0.1)
                    # Run on_shutdown callbacks, then hard-exit, skipping uvicorn's connection drain, which runs
                    # before lifespan shutdown and can hang forever on a ghost Windows connection (#5443).
                    if core.loop is not None and core.loop.is_running() and not core.app.is_stopped:
                        future = asyncio.run_coroutine_threadsafe(core.app.stop(), core.loop)
                        with suppress(Exception):
                            future.result(timeout=30)
                    sys.stdout.flush()
                    sys.stderr.flush()
                    os._exit(0)
                threading.Thread(target=monitor_shutdown_event, daemon=True).start()

        storage.set_storage_secret(self.config.storage_secret, self.config.session_middleware_kwargs)
        super().run(sockets=sockets)
