'''Lifecycle functions

You can register coroutines or functions to be called for the following events:

- `ui.lifecycle.on_startup`: Called when NiceGUI is started or restarted.
- `ui.lifecycle.on_shutdown`: Called when NiceGUI is shut down or restarted.
- `ui.lifecycle.on_connect`: Called for each client which connects. (nicegui.Client is passed as optional argument)
- `ui.lifecycle.on_disconnect`: Called for each client which disconnects. (nicegui.Client is passed as optional argument)

When NiceGUI is shut down or restarted, the all tasks still in execution will be automatically canceled.
'''
from typing import Awaitable, Callable, Union

from .. import globals


def on_connect(handler: Union[Callable, Awaitable]) -> None:
    '''Called every time a new client connects to NiceGUI.

    The callback has an optional parameter of `nicegui.Client`.'''

    globals.connect_handlers.append(handler)


def on_disconnect(handler: Union[Callable, Awaitable]) -> None:
    '''Called every time a new client disconnects from NiceGUI.

    The callback has an optional parameter of `nicegui.Client`.'''

    globals.disconnect_handlers.append(handler)


def on_startup(handler: Union[Callable, Awaitable]) -> None:
    if globals.state == globals.State.STARTED:
        raise RuntimeError('Unable to register another startup handler. NiceGUI has already been started.')
    globals.startup_handlers.append(handler)


def on_shutdown(handler: Union[Callable, Awaitable]) -> None:
    globals.shutdown_handlers.append(handler)


async def shutdown() -> None:
    '''Programmatically shut down NiceGUI.

    Only possible when auto-reload is disabled.'''

    if globals.reload:
        raise Exception('ui.shutdown is not supported when auto-reload is enabled')
    globals.server.should_exit = True
