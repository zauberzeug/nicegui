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

from . import background_tasks, globals, json  # pylint: disable=redefined-builtin
from .app import App
from .client import Client
from .dependencies import js_components, libraries
from .error import error_content
from .helpers import safe_invoke
from .json import NiceGUIJSONResponse
from .lifespan import lifespan
from .middlewares import RedirectWithPrefixMiddleware
from .page import page
from .version import __version__

globals.app = app = App(default_response_class=NiceGUIJSONResponse, lifespan=lifespan)
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
def _get_index(request: Request) -> Response:
    return globals.index_client.build_response(request)


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


@app.exception_handler(404)
async def _exception_handler_404(request: Request, exception: Exception) -> Response:
    globals.log.warning(f'{request.url} not found')
    with Client(page('')) as client:
        error_content(404, exception)
    return client.build_response(request, 404)


@app.exception_handler(Exception)
async def _exception_handler_500(request: Request, exception: Exception) -> Response:
    globals.log.exception(exception)
    with Client(page('')) as client:
        error_content(500, exception)
    return client.build_response(request, 500)


@sio.on('handshake')
async def _on_handshake(sid: str, client_id: str) -> bool:
    client = globals.clients.get(client_id)
    if not client:
        return False
    client.environ = sio.get_environ(sid)
    await sio.enter_room(sid, client.id)
    handle_handshake(client)
    return True


def handle_handshake(client: Client) -> None:
    """Cancel pending disconnect task and invoke connect handlers."""
    if client.disconnect_task:
        client.disconnect_task.cancel()
        client.disconnect_task = None
    for t in client.connect_handlers:
        safe_invoke(t, client)
    for t in globals.connect_handlers:
        safe_invoke(t, client)


@sio.on('disconnect')
def _on_disconnect(sid: str) -> None:
    query_bytes: bytearray = sio.get_environ(sid)['asgi.scope']['query_string']
    query = urllib.parse.parse_qs(query_bytes.decode())
    client_id = query['client_id'][0]
    client = globals.clients.get(client_id)
    if client:
        client.disconnect_task = background_tasks.create(handle_disconnect(client))


async def handle_disconnect(client: Client) -> None:
    """Wait for the browser to reconnect; invoke disconnect handlers if it doesn't."""
    delay = client.page.reconnect_timeout if client.page.reconnect_timeout is not None else globals.reconnect_timeout
    await asyncio.sleep(delay)
    if not client.shared:
        _delete_client(client)
    for t in client.disconnect_handlers:
        safe_invoke(t, client)
    for t in globals.disconnect_handlers:
        safe_invoke(t, client)


@sio.on('event')
def _on_event(_: str, msg: Dict) -> None:
    client = globals.clients.get(msg['client_id'])
    if not client or not client.has_socket_connection:
        return
    handle_event(client, msg)


def handle_event(client: Client, msg: Dict) -> None:
    """Forward an event to the corresponding element."""
    with client:
        sender = client.elements.get(msg['id'])
        if sender:
            msg['args'] = [None if arg is None else json.loads(arg) for arg in msg.get('args', [])]
            if len(msg['args']) == 1:
                msg['args'] = msg['args'][0]
            sender._handle_event(msg)  # pylint: disable=protected-access


@sio.on('javascript_response')
def _on_javascript_response(_: str, msg: Dict) -> None:
    client = globals.clients.get(msg['client_id'])
    if not client:
        return
    handle_javascript_response(client, msg)


def handle_javascript_response(client: Client, msg: Dict) -> None:
    """Forward a JavaScript response to the corresponding element."""
    client.waiting_javascript_commands[msg['request_id']] = msg['result']
