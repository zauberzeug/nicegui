import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi.responses import FileResponse

from . import (background_tasks, binding, favicon, globals, json, outbox,  # pylint: disable=redefined-builtin
               run_executor, welcome)
from .app import App
from .client import Client
from .helpers import is_file, safe_invoke


@asynccontextmanager
async def lifespan(app: App):
    """Handle the lifespan of the app (startup/shutdown)."""
    # NOTE ping interval and timeout need to be lower than the reconnect timeout, but can't be too low
    globals.sio.eio.ping_interval = max(globals.reconnect_timeout * 0.8, 4)
    globals.sio.eio.ping_timeout = max(globals.reconnect_timeout * 0.4, 2)
    if not globals.ui_run_has_been_called:
        raise RuntimeError('\n\n'
                           'You must call ui.run() to start the server.\n'
                           'If ui.run() is behind a main guard\n'
                           '   if __name__ == "__main__":\n'
                           'remove the guard or replace it with\n'
                           '   if __name__ in {"__main__", "__mp_main__"}:\n'
                           'to allow for multiprocessing.')
    if globals.favicon:
        if is_file(globals.favicon):
            globals.app.add_route('/favicon.ico', lambda _: FileResponse(globals.favicon))  # type: ignore
        else:
            globals.app.add_route('/favicon.ico', lambda _: favicon.get_favicon_response())
    else:
        globals.app.add_route('/favicon.ico', lambda _: FileResponse(Path(__file__).parent / 'static' / 'favicon.ico'))
    globals.state = globals.State.STARTING
    globals.loop = asyncio.get_running_loop()
    with globals.index_client:
        for t in globals.startup_handlers:
            safe_invoke(t)
    background_tasks.create(binding.refresh_loop(), name='refresh bindings')
    background_tasks.create(outbox.loop(), name='send outbox')
    background_tasks.create(prune_clients(), name='prune clients')
    background_tasks.create(prune_slot_stacks(), name='prune slot stacks')
    globals.state = globals.State.STARTED
    # if with_welcome_message:
    background_tasks.create(welcome.print_message())
    if globals.air:
        background_tasks.create(globals.air.connect())

    yield  # NOTE: this is where the app runs, everything below is shutdown

    if app.native.main_window:
        app.native.main_window.signal_server_shutdown()
    globals.state = globals.State.STOPPING
    with globals.index_client:
        for t in globals.shutdown_handlers:
            safe_invoke(t)
    run_executor.tear_down()
    globals.state = globals.State.STOPPED
    if globals.air:
        await globals.air.disconnect()


async def prune_clients() -> None:
    """Prune stale clients in an endless loop."""
    while True:
        try:
            stale_clients = [
                client
                for client in globals.clients.values()
                if not client.shared and not client.has_socket_connection and client.created < time.time() - 60.0
            ]
            for client in stale_clients:
                _delete_client(client)
        except Exception:
            # NOTE: make sure the loop doesn't crash
            globals.log.exception('Error while pruning clients')
        await asyncio.sleep(10)


def _delete_client(client: Client) -> None:
    """Delete a client and all its elements.

    If the global clients dictionary does not contain the client, its elements are still removed and a KeyError is raised.
    Normally this should never happen, but has been observed (see #1826).
    """
    client.remove_all_elements()
    del globals.clients[client.id]


async def prune_slot_stacks() -> None:
    """Prune stale slot stacks in an endless loop."""
    while True:
        try:
            running = [
                id(task)
                for task in asyncio.tasks.all_tasks()
                if not task.done() and not task.cancelled()
            ]
            stale = [
                id_
                for id_ in globals.slot_stacks
                if id_ not in running
            ]
            for id_ in stale:
                del globals.slot_stacks[id_]
        except Exception:
            # NOTE: make sure the loop doesn't crash
            globals.log.exception('Error while pruning slot stacks')
        await asyncio.sleep(10)
