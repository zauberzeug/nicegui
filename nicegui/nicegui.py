import asyncio
import os
import socket
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Optional

from fastapi import HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi_socketio import SocketManager

from nicegui import json
from nicegui.json import NiceGUIJSONResponse

from . import __version__, background_tasks, binding, favicon, globals, outbox
from .app import App
from .client import Client
from .dependencies import js_components, js_dependencies
from .element import Element
from .error import error_content
from .helpers import is_file, safe_invoke
from .page import page

globals.app = app = App(default_response_class=NiceGUIJSONResponse)
# NOTE we use custom json module which wraps orjson
socket_manager = SocketManager(app=app, mount_location='/_nicegui_ws/', json=json)
globals.sio = sio = socket_manager._sio

app.add_middleware(GZipMiddleware)
static_files = StaticFiles(
    directory=(Path(__file__).parent / 'static').resolve(),
    follow_symlink=True,
)
app.mount(f'/_nicegui/{__version__}/static', static_files, name='static')

globals.index_client = Client(page('/'), shared=True).__enter__()


@app.get('/')
def index(request: Request) -> Response:
    return globals.index_client.build_response(request)


@app.get(f'/_nicegui/{__version__}' + '/dependencies/{id}/{name}')
def get_dependencies(id: int, name: str):
    if id in js_dependencies and js_dependencies[id].path.exists() and js_dependencies[id].path.name == name:
        return FileResponse(js_dependencies[id].path, media_type='text/javascript')
    raise HTTPException(status_code=404, detail=f'dependency "{name}" with ID {id} not found')


@app.get(f'/_nicegui/{__version__}' + '/components/{name}')
def get_components(name: str):
    return FileResponse(js_components[name].path, media_type='text/javascript')


@app.on_event('startup')
def handle_startup(with_welcome_message: bool = True) -> None:
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
            globals.app.add_route('/favicon.ico', lambda _: FileResponse(globals.favicon))
        else:
            globals.app.add_route('/favicon.ico', lambda _: favicon.get_favicon_response())
    else:
        globals.app.add_route('/favicon.ico', lambda _: FileResponse(Path(__file__).parent / 'static' / 'favicon.ico'))
    globals.state = globals.State.STARTING
    globals.loop = asyncio.get_running_loop()
    with globals.index_client:
        for t in globals.startup_handlers:
            safe_invoke(t)
    background_tasks.create(binding.loop())
    background_tasks.create(outbox.loop())
    background_tasks.create(prune_clients())
    background_tasks.create(prune_slot_stacks())
    globals.state = globals.State.STARTED
    if with_welcome_message:
        print_welcome_message()


def print_welcome_message():
    host = os.environ['NICEGUI_HOST']
    port = os.environ['NICEGUI_PORT']
    ips = set()
    if host == '0.0.0.0':
        try:
            ips.update(set(info[4][0] for info in socket.getaddrinfo(socket.gethostname(), None) if len(info[4]) == 2))
        except Exception:
            pass  # NOTE: if we can't get the host's IP, we'll just use localhost
    ips.discard('127.0.0.1')
    addresses = [(f'http://{ip}:{port}' if port != '80' else f'http://{ip}') for ip in ['localhost'] + sorted(ips)]
    if len(addresses) >= 2:
        addresses[-1] = 'and ' + addresses[-1]
    print(f'NiceGUI ready to go on {", ".join(addresses)}')


@app.on_event('shutdown')
async def handle_shutdown() -> None:
    if app.native.main_window:
        app.native.main_window.signal_server_shutdown()
    globals.state = globals.State.STOPPING
    with globals.index_client:
        for t in globals.shutdown_handlers:
            safe_invoke(t)
    globals.state = globals.State.STOPPED


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
def handle_handshake(sid: str) -> bool:
    client = get_client(sid)
    if not client:
        return False
    client.environ = sio.get_environ(sid)
    sio.enter_room(sid, client.id)
    for t in client.connect_handlers:
        safe_invoke(t, client)
    for t in globals.connect_handlers:
        safe_invoke(t, client)
    return True


@sio.on('disconnect')
def handle_disconnect(sid: str) -> None:
    client = get_client(sid)
    if not client:
        return
    if not client.shared:
        delete_client(client.id)
    for t in client.disconnect_handlers:
        safe_invoke(t, client)
    for t in globals.disconnect_handlers:
        safe_invoke(t, client)


@sio.on('event')
def handle_event(sid: str, msg: Dict) -> None:
    client = get_client(sid)
    if not client or not client.has_socket_connection:
        return
    with client:
        sender = client.elements.get(msg['id'])
        if sender:
            sender._handle_event(msg)


@sio.on('javascript_response')
def handle_javascript_response(sid: str, msg: Dict) -> None:
    client = get_client(sid)
    if not client:
        return
    client.waiting_javascript_commands[msg['request_id']] = msg['result']


def get_client(sid: str) -> Optional[Client]:
    query_bytes: bytearray = sio.get_environ(sid)['asgi.scope']['query_string']
    query = urllib.parse.parse_qs(query_bytes.decode())
    client_id = query['client_id'][0]
    return globals.clients.get(client_id)


async def prune_clients() -> None:
    while True:
        stale = [
            id
            for id, client in globals.clients.items()
            if not client.shared and not client.has_socket_connection and client.created < time.time() - 60.0
        ]
        for id in stale:
            delete_client(id)
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


def delete_client(id: str) -> None:
    binding.remove(list(globals.clients[id].elements.values()), Element)
    for element in globals.clients[id].elements.values():
        element.delete()
    del globals.clients[id]
