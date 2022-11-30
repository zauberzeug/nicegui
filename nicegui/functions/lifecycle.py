from typing import Awaitable, Callable, Union

from .. import globals


def on_connect(handler: Union[Callable, Awaitable]) -> None:
    globals.get_client().connect_handlers.append(handler)


def on_disconnect(handler: Union[Callable, Awaitable]) -> None:
    globals.get_client().disconnect_handlers.append(handler)


def on_startup(handler: Union[Callable, Awaitable]) -> None:
    if globals.state == globals.State.STARTED:
        raise RuntimeError('Unable to register another startup handler. NiceGUI has already been started.')
    globals.startup_handlers.append(handler)


def on_shutdown(handler: Union[Callable, Awaitable]) -> None:
    globals.shutdown_handlers.append(handler)


async def shutdown() -> None:
    if globals.reload:
        raise Exception('ui.shutdown is not supported when auto-reload is enabled')
    globals.server.should_exit = True
