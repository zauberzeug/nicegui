import asyncio
import mimetypes
import time
import urllib.parse
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List

import socketio
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse, Response

from . import air, background_tasks, binding, core, favicon, helpers, json, run, welcome
from .app import App
from .client import Client
from .dependencies import dynamic_resources, js_components, libraries, resources
from .error import error_content
from .json import NiceGUIJSONResponse
from .logging import log
from .page import page
from .persistence import PersistentDict
from .slot import Slot
from .staticfiles import CacheControlledStaticFiles
from .version import __version__


@asynccontextmanager
async def _lifespan(_: App):
    await _startup()
    yield
    await _shutdown()


class SocketIoApp(socketio.ASGIApp):
    """Custom ASGI app to handle root_path.

    This is a workaround for https://github.com/miguelgrinberg/python-engineio/pull/345
    """

    async def __call__(self, scope, receive, send):
        root_path = scope.get('root_path')
        if root_path and scope['path'].startswith(root_path):
            scope['path'] = scope['path'][len(root_path):]
        return await super().__call__(scope, receive, send)


core.app = app = App(default_response_class=NiceGUIJSONResponse, lifespan=_lifespan)
core.app.storage.general.initialize_sync()
core.sio = sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', json=json)  # custom orjson wrapper
sio_app = SocketIoApp(socketio_server=sio, socketio_path='/socket.io')
app.mount('/_nicegui_ws/', sio_app)


mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('text/css', '.css')

static_files = CacheControlledStaticFiles(
    directory=(Path(__file__).parent / 'static').resolve(),
    follow_symlink=True,
)
app.mount(f'/_nicegui/{__version__}/static', static_files, name='static')

Client.auto_index_client = Client(page('/'), request=None).__enter__()  # pylint: disable=unnecessary-dunder-call


@app.get('/')
def _get_index(request: Request) -> Response:
    return Client.auto_index_client.build_response(request)


@app.get(f'/_nicegui/{__version__}' + '/libraries/{key:path}')
def _get_library(key: str) -> FileResponse:
    is_map = key.endswith('.map')
    dict_key = key[:-4] if is_map else key
    if dict_key in libraries:
        path = libraries[dict_key].path
        if is_map:
            path = path.with_name(path.name + '.map')
        if path.exists():
            return FileResponse(path, media_type='text/javascript')
    raise HTTPException(status_code=404, detail=f'library "{key}" not found')


@app.get(f'/_nicegui/{__version__}' + '/components/{key:path}')
def _get_component(key: str) -> FileResponse:
    if key in js_components and js_components[key].path.exists():
        return FileResponse(js_components[key].path, media_type='text/javascript')
    raise HTTPException(status_code=404, detail=f'component "{key}" not found')


@app.get(f'/_nicegui/{__version__}' + '/resources/{key}/{path:path}')
def _get_resource(key: str, path: str) -> FileResponse:
    if key in resources:
        filepath = resources[key].path / path
        try:
            filepath.resolve().relative_to(resources[key].path.resolve())  # NOTE: use is_relative_to() in Python 3.9
        except ValueError as e:
            raise HTTPException(status_code=403, detail='forbidden') from e
        if filepath.exists():
            media_type, _ = mimetypes.guess_type(filepath)
            return FileResponse(filepath, media_type=media_type)
    raise HTTPException(status_code=404, detail=f'resource "{key}" not found')


@app.get(f'/_nicegui/{__version__}' + '/dynamic_resources/{name}')
def _get_dynamic_resource(name: str) -> Response:
    if name in dynamic_resources:
        return dynamic_resources[name].function()
    raise HTTPException(status_code=404, detail=f'dynamic resource "{name}" not found')


async def _startup() -> None:
    """Handle the startup event."""
    if not app.config.has_run_config:
        raise RuntimeError('\n\n'
                           'You must call ui.run() to start the server.\n'
                           'If ui.run() is behind a main guard\n'
                           '   if __name__ == "__main__":\n'
                           'remove the guard or replace it with\n'
                           '   if __name__ in {"__main__", "__mp_main__"}:\n'
                           'to allow for multiprocessing.')
    await welcome.collect_urls()
    # NOTE ping interval and timeout need to be lower than the reconnect timeout, but can't be too low
    sio.eio.ping_interval = max(app.config.reconnect_timeout * 0.8, 4)
    sio.eio.ping_timeout = max(app.config.reconnect_timeout * 0.4, 2)
    if core.app.config.favicon:
        if helpers.is_file(core.app.config.favicon):
            app.add_route('/favicon.ico', lambda _: FileResponse(core.app.config.favicon))  # type: ignore
        else:
            app.add_route('/favicon.ico', lambda _: favicon.get_favicon_response())
    else:
        app.add_route('/favicon.ico', lambda _: FileResponse(Path(__file__).parent / 'static' / 'favicon.ico'))
    core.loop = asyncio.get_running_loop()
    run.setup()
    app.start()
    background_tasks.create(binding.refresh_loop(), name='refresh bindings')
    app.timer(10, Client.prune_instances, immediate=False)
    app.timer(10, Slot.prune_stacks, immediate=False)
    app.timer(10, prune_tab_storage, immediate=False)
    if app.storage.secret is not None:
        app.timer(10, prune_user_storage, immediate=False)
    air.connect()


async def _shutdown() -> None:
    """Handle the shutdown event."""
    if app.native.main_window:
        app.native.main_window.signal_server_shutdown()
    air.disconnect()
    await app.stop()
    run.tear_down()


@app.exception_handler(404)
async def _exception_handler_404(request: Request, exception: Exception) -> Response:
    log.warning(f'{request.url} not found')
    with Client(page(''), request=request) as client:
        error_content(404, exception)
    return client.build_response(request, 404)


@app.exception_handler(Exception)
async def _exception_handler_500(request: Request, exception: Exception) -> Response:
    log.exception(exception)
    with Client(page(''), request=request) as client:
        error_content(500, exception)
    return client.build_response(request, 500)


@sio.on('handshake')
async def _on_handshake(sid: str, data: Dict[str, Any]) -> bool:
    client = Client.instances.get(data['client_id'])
    if not client:
        return False
    if data.get('old_tab_id'):
        app.storage.copy_tab(data['old_tab_id'], data['tab_id'])
    client.tab_id = data['tab_id']
    if sid[:5].startswith('test-'):
        client.environ = {'asgi.scope': {'description': 'test client', 'type': 'test'}}
    else:
        client.environ = sio.get_environ(sid)
        await sio.enter_room(sid, client.id)
    client.handle_handshake(sid, data['document_id'], data.get('next_message_id'))
    assert client.tab_id is not None
    await core.app.storage._create_tab_storage(client.tab_id)  # pylint: disable=protected-access
    return True


@sio.on('disconnect')
def _on_disconnect(sid: str) -> None:
    query_bytes: bytearray = sio.get_environ(sid)['asgi.scope']['query_string']
    query = urllib.parse.parse_qs(query_bytes.decode())
    client_id = query['client_id'][0]
    client = Client.instances.get(client_id)
    if client:
        client.handle_disconnect(sid)


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


@sio.on('ack')
def _on_ack(_: str, msg: Dict) -> None:
    client = Client.instances.get(msg['client_id'])
    if not client:
        return
    client.outbox.prune_history(msg['next_message_id'])


async def prune_tab_storage(*, force: bool = False) -> None:
    """Prune tab storage that is older than the configured ``max_tab_storage_age``."""
    tab_storages = core.app.storage._tabs  # pylint: disable=protected-access
    for tab_id, tab in list(tab_storages.items()):
        if force or time.time() > tab.last_modified + core.app.storage.max_tab_storage_age:
            tab.clear()
            if isinstance(tab, PersistentDict):
                await tab.close()
            del tab_storages[tab_id]


async def prune_user_storage(*, force: bool = False) -> None:
    """Remove user storage objects without a client session."""
    client_session_ids = {client.request.session['id']
                          for client in Client.instances.values()
                          if client.request is not None}
    storages_to_close: List[PersistentDict] = []
    now = time.time()
    user_storages = core.app.storage._users  # pylint: disable=protected-access
    for session_id in list(user_storages):
        if session_id not in client_session_ids:
            age = now - user_storages[session_id].last_modified
            if force or age > 10.0:  # NOTE: do not remove storages created by middleware and still wait for client
                storages_to_close.append(user_storages.pop(session_id))
    results = await asyncio.gather(*[storage.close() for storage in storages_to_close], return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            log.exception(result)
