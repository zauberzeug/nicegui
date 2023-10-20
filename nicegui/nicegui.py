import asyncio
import mimetypes
import urllib.parse
from pathlib import Path
from typing import Dict

from fastapi import HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi_socketio import SocketManager

from . import (air, background_tasks, binding, favicon, globals, json, outbox,  # pylint: disable=redefined-builtin
               run_executor, welcome)
from .app import App
from .client import Client
from .dependencies import js_components, libraries
from .error import error_content
from .helpers import is_file
from .json import NiceGUIJSONResponse
from .logging import log
from .middlewares import RedirectWithPrefixMiddleware
from .page import page
from .version import __version__

globals.app = app = App(default_response_class=NiceGUIJSONResponse)
# NOTE we use custom json module which wraps orjson
socket_manager = SocketManager(app=app, mount_location='/_nicegui_ws/', json=json)
globals.sio = sio = socket_manager._sio  # pylint: disable=protected-access

mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('text/css', '.css')

app.add_middleware(GZipMiddleware)
app.add_middleware(RedirectWithPrefixMiddleware)
static_files = StaticFiles(
    directory=(Path(__file__).parent / 'static').resolve(),
    follow_symlink=True,
)
app.mount(f'/_nicegui/{__version__}/static', static_files, name='static')

Client.index_client = Client(page('/'), shared=True).__enter__()  # pylint: disable=unnecessary-dunder-call


@app.get('/')
def _get_index(request: Request) -> Response:
    return Client.index_client.build_response(request)


@app.get(f'/_nicegui/{__version__}' + '/libraries/{key:path}')
def _get_library(key: str) -> FileResponse:
    is_map = key.endswith('.map')
    dict_key = key[:-4] if is_map else key
    if dict_key in libraries:
        path = libraries[dict_key].path
        if is_map:
            path = path.with_name(path.name + '.map')
        if path.exists():
            headers = {'Cache-Control': 'public, max-age=3600'}
            return FileResponse(path, media_type='text/javascript', headers=headers)
    raise HTTPException(status_code=404, detail=f'library "{key}" not found')


@app.get(f'/_nicegui/{__version__}' + '/components/{key:path}')
def _get_component(key: str) -> FileResponse:
    if key in js_components and js_components[key].path.exists():
        headers = {'Cache-Control': 'public, max-age=3600'}
        return FileResponse(js_components[key].path, media_type='text/javascript', headers=headers)
    raise HTTPException(status_code=404, detail=f'component "{key}" not found')


@app.on_event('startup')
def handle_startup(with_welcome_message: bool = True) -> None:
    """Handle the startup event."""
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
            app.add_route('/favicon.ico', lambda _: FileResponse(globals.favicon))  # type: ignore
        else:
            app.add_route('/favicon.ico', lambda _: favicon.get_favicon_response())
    else:
        app.add_route('/favicon.ico', lambda _: FileResponse(Path(__file__).parent / 'static' / 'favicon.ico'))
    globals.loop = asyncio.get_running_loop()
    globals.app.start()
    background_tasks.create(binding.refresh_loop(), name='refresh bindings')
    background_tasks.create(outbox.loop(air.instance), name='send outbox')
    background_tasks.create(Client.prune_instances(), name='prune clients')
    background_tasks.create(prune_slot_stacks(), name='prune slot stacks')
    if with_welcome_message:
        background_tasks.create(welcome.print_message())
    air.connect()


@app.on_event('shutdown')
async def handle_shutdown() -> None:
    """Handle the shutdown event."""
    if app.native.main_window:
        app.native.main_window.signal_server_shutdown()
    globals.app.stop()
    run_executor.tear_down()
    air.disconnect()


@app.exception_handler(404)
async def _exception_handler_404(request: Request, exception: Exception) -> Response:
    log.warning(f'{request.url} not found')
    with Client(page('')) as client:
        error_content(404, exception)
    return client.build_response(request, 404)


@app.exception_handler(Exception)
async def _exception_handler_500(request: Request, exception: Exception) -> Response:
    log.exception(exception)
    with Client(page('')) as client:
        error_content(500, exception)
    return client.build_response(request, 500)


@sio.on('handshake')
async def _on_handshake(sid: str, client_id: str) -> bool:
    client = Client.instances.get(client_id)
    if not client:
        return False
    client.environ = sio.get_environ(sid)
    await sio.enter_room(sid, client.id)
    client.handle_handshake()
    return True


@sio.on('disconnect')
def _on_disconnect(sid: str) -> None:
    query_bytes: bytearray = sio.get_environ(sid)['asgi.scope']['query_string']
    query = urllib.parse.parse_qs(query_bytes.decode())
    client_id = query['client_id'][0]
    client = Client.instances.get(client_id)
    if client:
        client.handle_disconnect()


@sio.on('event')
def _on_event(_: str, msg: Dict) -> None:
    client = Client.instances.get(msg['client_id'])
    if not client or not client.has_socket_connection:
        return
    client.handle_event(msg)


@sio.on('javascript_response')
def _on_javascript_response(_: str, msg: Dict) -> None:
    client = Client.instances.get(msg['client_id'])
    if not client:
        return
    client.handle_javascript_response(msg)


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
            log.exception('Error while pruning slot stacks')
        await asyncio.sleep(10)
