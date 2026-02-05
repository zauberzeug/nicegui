import asyncio
import inspect
import mimetypes
import time
import urllib.parse
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import socketio
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse, Response

from . import air, background_tasks, binding, core, favicon, helpers, json, run, welcome
from .app import App
from .client import Client
from .dependencies import dynamic_resources, esm_modules, js_components, libraries, resources, vue_components
from .error import error_content
from .json import NiceGUIJSONResponse
from .logging import log
from .page import page
from .page_arguments import PageArguments
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
mimetypes.add_type('text/javascript', '.mjs')
mimetypes.add_type('text/css', '.css')

static_files = CacheControlledStaticFiles(
    directory=(Path(__file__).parent / 'static').resolve(),
    follow_symlink=True,
)
app.mount(f'/_nicegui/{__version__}/static', static_files, name='static')


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
def _get_component(key: str) -> Response:
    if key in js_components and js_components[key].path.exists():
        return FileResponse(js_components[key].path, media_type='text/javascript')
    elif key in vue_components:
        return Response(vue_components[key].script, media_type='text/javascript')
    raise HTTPException(status_code=404, detail=f'component "{key}" not found')


@app.get(f'/_nicegui/{__version__}' + '/resources/{key}/{path:path}')
def _get_resource(key: str, path: str) -> FileResponse:
    if key in resources:
        filepath = resources[key].path / path
        if not filepath.resolve().is_relative_to(resources[key].path.resolve()):
            raise HTTPException(status_code=403, detail='forbidden')
        if filepath.exists():
            media_type, _ = mimetypes.guess_type(filepath)
            return FileResponse(filepath, media_type=media_type)
    raise HTTPException(status_code=404, detail=f'resource "{key}" not found')


@app.get(f'/_nicegui/{__version__}' + '/dynamic_resources/{name}')
def _get_dynamic_resource(name: str) -> Response:
    if name in dynamic_resources:
        return dynamic_resources[name].function()
    raise HTTPException(status_code=404, detail=f'dynamic resource "{name}" not found')


@app.get(f'/_nicegui/{__version__}' + '/esm/{key}/{path:path}')
def _get_esm(key: str, path: str) -> FileResponse:
    if key in esm_modules:
        filepath = esm_modules[key].path / path
        if not filepath.resolve().is_relative_to(esm_modules[key].path.resolve()):
            raise HTTPException(status_code=403, detail='forbidden')
        if filepath.exists():
            media_type, _ = mimetypes.guess_type(filepath)
            return FileResponse(filepath, media_type=media_type)
    raise HTTPException(status_code=404, detail=f'ESM module "{key}" not found')


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
    app.timer(10, Client.prune_instances)
    app.timer(10, Slot.prune_stacks)
    app.timer(10, prune_tab_storage)
    if app.storage.secret is not None:
        app.timer(10, prune_user_storage)
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
    root = core.root
    if root is not None:
        kwargs = {
            name: PageArguments._convert_parameter(  # pylint: disable=protected-access
                request.query_params[name],
                param.annotation,
            )
            for name, param in inspect.signature(root).parameters.items()
            if name in request.query_params and name != 'request'
        }
        return await page('')._wrap(root)(request=request, **kwargs)  # pylint: disable=protected-access
    log.warning(f'{request.url} not found')
    with Client(page(''), request=request) as client:
        error_content(404, exception)
    return client.build_response(request, 404)


@app.exception_handler(Exception)
async def _exception_handler_500(request: Request, exception: Exception) -> Response:
    if not request.scope.get('nicegui_page_path'):
        raise exception  # Simply return "Internal Server Error", just like FastAPI would do
    log.exception(exception)
    with Client(page(''), request=request) as client:
        error_content(500, exception)
    return client.build_response(request, 500)


@sio.on('connect')
async def _on_connect(sid: str, data: dict[str, Any], _=None) -> None:
    query = {k: v[0] for k, v in urllib.parse.parse_qs(data.get('QUERY_STRING', '')).items()}
    if query.get('implicit_handshake', '') == 'true' and not await _on_handshake(sid, query):
        raise socketio.exceptions.ConnectionRefusedError('Implicit handshake failed')


@sio.on('handshake')
async def _on_handshake(sid: str, data: dict[str, Any]) -> bool:
    client = Client.instances.get(data['client_id'])
    if not client:
        return False
    if data.get('old_tab_id'):
        app.storage.copy_tab(data['old_tab_id'], data['tab_id'])
    client.tab_id = data['tab_id']
    if sid.startswith('test-'):
        client.environ = {'asgi.scope': {'description': 'test client', 'type': 'test'}}
    else:
        client.environ = sio.get_environ(sid)
        await sio.enter_room(sid, client.id)
    client.handle_handshake(sid, data['document_id'],
                            int(data['next_message_id']) if 'next_message_id' in data else None)
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
def _on_event(_: str, msg: dict) -> None:
    client = Client.instances.get(msg['client_id'])
    if not client or not client.has_socket_connection:
        return
    client.handle_event(msg)


@sio.on('javascript_response')
def _on_javascript_response(_: str, msg: dict) -> None:
    if client := Client.instances.get(msg['client_id']):
        client.handle_javascript_response(msg)


@sio.on('ack')
def _on_ack(_: str, msg: dict) -> None:
    if client := Client.instances.get(msg['client_id']):
        client.outbox.prune_history(msg['next_message_id'])


@sio.on('log')
def _on_log(_: str, msg: dict) -> None:
    if client := Client.instances.get(msg['client_id']):
        client.handle_log_message(msg)


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
    client_session_ids = {client.request.session['id'] for client in Client.instances.values()}
    storages_to_close: list[PersistentDict] = []
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
