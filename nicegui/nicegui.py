import asyncio
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi_socketio import SocketManager

from . import binding, globals
from .client import Client
from .dependencies import js_components, js_dependencies
from .element import Element
from .error import error_content
from .helpers import safe_invoke
from .page import page
from .task_logger import create_task

globals.app = app = FastAPI()
globals.sio = sio = SocketManager(app=app)._sio

app.add_middleware(GZipMiddleware)
app.mount('/_nicegui/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')

globals.index_client = Client(page('/'), shared=True).__enter__()


@app.get('/')
def index(request: Request) -> Response:
    return globals.index_client.build_response(request)


@app.get('/_nicegui/dependencies/{id}/{name}')
def get_dependencies(id: int, name: str):
    if id in js_dependencies and js_dependencies[id].path.exists() and js_dependencies[id].path.name == name:
        return FileResponse(js_dependencies[id].path, media_type='text/javascript')
    raise HTTPException(status_code=404, detail=f'dependency "{name}" with ID {id} not found')


@app.get('/_nicegui/components/{name}')
def get_components(name: str):
    return FileResponse(js_components[name].path, media_type='text/javascript')


@app.on_event('startup')
def handle_startup(with_welcome_message: bool = True) -> None:
    globals.state = globals.State.STARTING
    globals.loop = asyncio.get_running_loop()
    for t in globals.startup_handlers:
        safe_invoke(t)
    create_task(binding.loop())
    create_task(prune_clients())
    create_task(prune_slot_stacks())
    globals.state = globals.State.STARTED
    if with_welcome_message:
        print(f'NiceGUI ready to go on http://{globals.host}:{globals.port}')


@app.on_event('shutdown')
def handle_shutdown() -> None:
    globals.state = globals.State.STOPPING
    for t in globals.shutdown_handlers:
        safe_invoke(t)
    for t in globals.tasks:
        t.cancel()
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
async def handle_handshake(sid: str) -> bool:
    client = get_client(sid)
    if not client:
        return False
    client.environ = sio.get_environ(sid)
    sio.enter_room(sid, client.id)
    for t in client.connect_handlers:
        safe_invoke(t, client)
    return True


@sio.on('disconnect')
async def handle_disconnect(sid: str) -> None:
    client = get_client(sid)
    if not client:
        return
    if not client.shared:
        delete_client(client.id)
    for t in client.disconnect_handlers:
        safe_invoke(t, client)


@sio.on('event')
def handle_event(sid: str, msg: Dict) -> None:
    client = get_client(sid)
    if not client or not client.has_socket_connection:
        return
    with client:
        sender = client.elements.get(msg['id'])
        if sender:
            sender.handle_event(msg)


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
    del globals.clients[id]
