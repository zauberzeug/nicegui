from typing import Awaitable, Callable, Union

import justpy as jp

from . import globals


def on_connect(self, handler: Union[Callable, Awaitable]):
    globals.connect_handlers.append(handler)


def on_disconnect(self, handler: Union[Callable, Awaitable]):
    globals.disconnect_handlers.append(handler)


def on_startup(self, handler: Union[Callable, Awaitable]):
    globals.startup_handlers.append(handler)


def on_shutdown(self, handler: Union[Callable, Awaitable]):
    globals.shutdown_handlers.append(handler)


async def shutdown(self) -> None:
    if globals.config.reload:
        raise Exception('ui.shutdown is not supported when auto-reload is enabled')
    for socket in [s for page in jp.WebPage.sockets.values() for s in page.values()]:
        await socket.close()
    globals.server.should_exit = True
