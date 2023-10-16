import asyncio
import mimetypes
import time
import urllib.parse
from pathlib import Path
from typing import Dict

from fastapi import HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi_socketio import SocketManager

from . import (background_tasks, binding, favicon, globals, json, outbox,  # pylint: disable=redefined-builtin
               run_executor, welcome)
from .app import App
from .client import Client
from .dependencies import js_components, libraries
from .error import error_content
from .helpers import is_file, safe_invoke
from .json import NiceGUIJSONResponse
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

globals.index_client = Client(page('/'), shared=True).__enter__()  # pylint: disable=unnecessary-dunder-call


@app.get('/')
def index(request: Request) -> Response:
    return globals.index_client.build_response(request)


@app.get(f'/_nicegui/{__version__}' + '/libraries/{key:path}')
def get_library(key: str) -> FileResponse:
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
def get_component(key: str) -> FileResponse:
    if key in js_components and js_components[key].path.exists():
        headers = {'Cache-Control': 'public, max-age=3600'}
        return FileResponse(js_components[key].path, media_type='text/javascript', headers=headers)
    raise HTTPException(status_code=404, detail=f'component "{key}" not found')


@app.on_event('startup')
def handle_startup(with_welcome_message: bool = True) -> None:
    if globals.reconnect_timeout > 0:  # TODO in 1.4 we DEPRECATED a value of 0 and should remove this check
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
    if with_welcome_message:
        background_tasks.create(welcome.print_message())
    if globals.air:
        background_tasks.create(globals.air.connect())


@app.on_event('shutdown')
async def handle_shutdown() -> None:
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


@app.exception_handler(404)
async def exception_handler_404(request: Request, exception: Exception) -> Response:
    globals.log.warning(f'{request.url} not found')
    with Client(page('')) as client:
        error_content(404, exception)
    return client.build_response(request, 404)


@app.exception_handler(Exception)
async def exception_handler_500(request: Request, exception: Exception) -> Response:
    globals.log.exception(exception)
    with Client(page('')) as client:
        error_content(500, exception)
    return client.build_response(request, 500)


@sio.on('handshake')
async def on_handshake(sid: str, client_id: str) -> bool:
    client = globals.clients.get(client_id)
    if not client:
        return False
    client.environ = sio.get_environ(sid)
    await sio.enter_room(sid, client.id)
    handle_handshake(client)
    return True


def handle_handshake(client: Client) -> None:
    if client.disconnect_task:
        client.disconnect_task.cancel()
        client.disconnect_task = None
    for t in client.connect_handlers:
        safe_invoke(t, client)
    for t in globals.connect_handlers:
        safe_invoke(t, client)


@sio.on('disconnect')
def on_disconnect(sid: str) -> None:
    query_bytes: bytearray = sio.get_environ(sid)['asgi.scope']['query_string']
    query = urllib.parse.parse_qs(query_bytes.decode())
    client_id = query['client_id'][0]
    client = globals.clients.get(client_id)
    if client:
        client.disconnect_task = background_tasks.create(handle_disconnect(client))


async def handle_disconnect(client: Client) -> None:
    delay = client.page.reconnect_timeout if client.page.reconnect_timeout is not None else globals.reconnect_timeout
    await asyncio.sleep(delay)
    if not client.shared:
        delete_client(client.id)
    for t in client.disconnect_handlers:
        safe_invoke(t, client)
    for t in globals.disconnect_handlers:
        safe_invoke(t, client)


@sio.on('event')
def on_event(_: str, msg: Dict) -> None:
    client = globals.clients.get(msg['client_id'])
    if not client or not client.has_socket_connection:
        return
    handle_event(client, msg)


def handle_event(client: Client, msg: Dict) -> None:
    with client:
        sender = client.elements.get(msg['id'])
        if sender:
            msg['args'] = [None if arg is None else json.loads(arg) for arg in msg.get('args', [])]
            if len(msg['args']) == 1:
                msg['args'] = msg['args'][0]
            sender._handle_event(msg)  # pylint: disable=protected-access


@sio.on('javascript_response')
def on_javascript_response(_: str, msg: Dict) -> None:
    client = globals.clients.get(msg['client_id'])
    if not client:
        return
    handle_javascript_response(client, msg)


def handle_javascript_response(client: Client, msg: Dict) -> None:
    client.waiting_javascript_commands[msg['request_id']] = msg['result']


async def prune_clients() -> None:
    while True:
        stale_clients = [
            id
            for id, client in globals.clients.items()
            if not client.shared and not client.has_socket_connection and client.created < time.time() - 60.0
        ]
        for client_id in stale_clients:
            delete_client(client_id)
        await asyncio.sleep(10)


async def prune_slot_stacks() -> None:
    while True:
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
        await asyncio.sleep(10)


def delete_client(client_id: str) -> None:
    globals.clients.pop(client_id).remove_all_elements()
