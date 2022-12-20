import asyncio
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_socketio import SocketManager

from . import binding, globals, vue
from .client import Client
from .element import Element
from .error import error_content
from .favicon import create_favicon_routes
from .helpers import safe_invoke
from .page import page
from .task_logger import create_task

globals.app = app = FastAPI()
globals.sio = sio = SocketManager(app=app)._sio

app.add_middleware(GZipMiddleware)
app.mount('/_nicegui/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')

globals.index_client = Client(page('/'), shared=True).__enter__()


@app.get('/')
def index(request: Request) -> str:
    return globals.index_client.build_response(request)


@app.get('/_nicegui/dependencies/{id}/{name}')
def vue_dependencies(id: int, name: str):
    if id in vue.js_dependencies and vue.js_dependencies[id].path.exists():
        return FileResponse(vue.js_dependencies[id].path, media_type='text/javascript')
    raise HTTPException(status_code=404, detail=f'dependency "{name}" with ID {id} not found')


@app.get('/_nicegui/components/{name}')
def vue_dependencies(name: str):
    return FileResponse(vue.js_components[name].path, media_type='text/javascript')


@app.on_event('startup')
def handle_startup(with_welcome_message: bool = True) -> None:
    globals.state = globals.State.STARTING
    globals.loop = asyncio.get_running_loop()
    create_favicon_routes()
    [safe_invoke(t) for t in globals.startup_handlers]
    create_task(binding.loop())
    create_task(prune_clients())
    globals.state = globals.State.STARTED
    if with_welcome_message:
        print(f'NiceGUI ready to go on http://{globals.host}:{globals.port}')


@app.on_event('shutdown')
def handle_shutdown() -> None:
    globals.state = globals.State.STOPPING
    [safe_invoke(t) for t in globals.shutdown_handlers]
    [t.cancel() for t in globals.tasks]
    globals.state = globals.State.STOPPED


@app.exception_handler(404)
async def exception_handler(request: Request, exception: Exception):
    globals.log.warning(f'{request.url} not found')
    with Client(page('')) as client:
        error_content(404, exception)
    return client.build_response(request, 404)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exception: Exception):
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
    with client:
        [safe_invoke(t) for t in client.connect_handlers]
    return True


@sio.on('disconnect')
async def handle_disconnect(sid: str) -> None:
    client = get_client(sid)
    if not client:
        return
    if not client.shared:
        delete_client(client.id)
    with client:
        [safe_invoke(t) for t in client.disconnect_handlers]


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
def handle_event(sid: str, msg: Dict) -> None:
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


def delete_client(id: str) -> None:
    binding.remove(list(globals.clients[id].elements.values()), Element)
    del globals.clients[id]
