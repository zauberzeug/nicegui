from typing import Awaitable, Callable, Union

from .globals import connect_handlers, disconnect_handlers, shutdown_handlers, startup_handlers


def on_connect(self, handler: Union[Callable, Awaitable]):
    connect_handlers.append(handler)


def on_disconnect(self, handler: Union[Callable, Awaitable]):
    disconnect_handlers.append(handler)


def on_startup(self, handler: Union[Callable, Awaitable]):
    startup_handlers.append(handler)


def on_shutdown(self, handler: Union[Callable, Awaitable]):
    shutdown_handlers.append(handler)
