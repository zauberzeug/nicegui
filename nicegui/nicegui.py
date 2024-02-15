import asyncio
import mimetypes
import urllib.parse
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict

import socketio
from fastapi import HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from . import air, background_tasks, binding, core, favicon, helpers, json, run, welcome
from .app import App
from .client import Client
from .dependencies import js_components, libraries, resources
from .error import error_content
from .json import NiceGUIJSONResponse
from .logging import log
from .middlewares import RedirectWithPrefixMiddleware
from .page import page
from .slot import Slot
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
# NOTE we use custom json module which wraps orjson
core.sio = sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', json=json)
sio_app = SocketIoApp(socketio_server=sio, socketio_path='/socket.io')
app.mount('/_nicegui_ws/', sio_app)


mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('text/css', '.css')

app.add_middleware(GZipMiddleware)
app.add_middleware(RedirectWithPrefixMiddleware)
static_files = StaticFiles(
    directory=(Path(__file__).parent / 'static').resolve(),
    follow_symlink=True,
)
app.mount(f'/_nicegui/{__version__}/static', static_files, name='static')

Client.auto_index_client = Client(page('/'), shared=True).__enter__()  # pylint: disable=unnecessary-dunder-call


@app.get('/')
def _get_index(request: Request) -> Response:
    """
    Retrieves the index page for the NiceGUI application.

    This function is responsible for building and returning the index page
    for the NiceGUI application. It delegates the actual building of the
    response to the auto_index_client.

    Parameters:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response object representing the index page.

    """
    return Client.auto_index_client.build_response(request)


@app.get(f'/_nicegui/{__version__}' + '/libraries/{key:path}')
def _get_library(key: str) -> FileResponse:
    """
    Retrieves a library file based on the provided key.

    Args:
        key (str): The key used to identify the library file.

    Returns:
        FileResponse: The library file response.

    Raises:
        HTTPException: If the library file is not found.

    Notes:
        - The key should be the filename of the library file.
        - If the key ends with '.map', it is treated as a map file and the corresponding library file is retrieved.
        - The 'libraries' dictionary is used to lookup the path of the library file.
        - If the library file is found, a FileResponse object is returned with the appropriate media type and headers.
        - If the library file is not found, an HTTPException with status code 404 is raised.
    """
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
    """
    Retrieve a component file based on the provided key.

    Args:
        key (str): The key of the component to retrieve.

    Returns:
        FileResponse: The file response containing the component file.

    Raises:
        HTTPException: If the component file with the provided key is not found.

    """
    if key in js_components and js_components[key].path.exists():
        headers = {'Cache-Control': 'public, max-age=3600'}
        return FileResponse(js_components[key].path, media_type='text/javascript', headers=headers)
    raise HTTPException(status_code=404, detail=f'component "{key}" not found')


@app.get(f'/_nicegui/{__version__}' + '/resources/{key}/{path:path}')
def _get_resource(key: str, path: str) -> FileResponse:
    """
    Retrieves a resource file based on the given key and path.

    Args:
        key (str): The key to identify the resource.
        path (str): The path to the resource file.

    Returns:
        FileResponse: The file response object containing the resource file.

    Raises:
        HTTPException: If the resource file is not found.

    Notes:
        - This function checks if the specified key exists in the resources dictionary.
        - If the key exists, it constructs the file path by appending the given path to the resource's base path.
        - If the file exists at the constructed path, it creates a FileResponse object with the appropriate media type and headers.
        - The function raises an HTTPException with a status code of 404 if the resource file is not found.
    """
    if key in resources:
        filepath = resources[key].path / path
        if filepath.exists():
            headers = {'Cache-Control': 'public, max-age=3600'}
            media_type, _ = mimetypes.guess_type(filepath)
            return FileResponse(filepath, media_type=media_type, headers=headers)
    raise HTTPException(status_code=404, detail=f'resource "{key}" not found')


async def _startup() -> None:
    """Handle the startup event.

    This function is responsible for handling the startup event of the server. It performs various tasks
    such as setting up the server configuration, collecting URLs, setting ping intervals and timeouts,
    adding routes for favicon, starting the server, and creating background tasks.

    Usage:
        This function should be called to handle the startup event of the server. It is typically called
        within the main function or entry point of the application.

    Raises:
        RuntimeError: If `ui.run()` has not been called to start the server. To resolve this, ensure that
            `ui.run()` is called before invoking this function. If `ui.run()` is behind a main guard,
            replace the guard with `if __name__ in {"__main__", "__mp_main__"}:` to allow for multiprocessing.

    """
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
    app.start()
    background_tasks.create(binding.refresh_loop(), name='refresh bindings')
    background_tasks.create(Client.prune_instances(), name='prune clients')
    background_tasks.create(Slot.prune_stacks(), name='prune slot stacks')
    air.connect()


async def _shutdown() -> None:
    """Handle the shutdown event.

    This function is responsible for handling the shutdown event in the application.
    It performs the following actions:
    1. Signals the main window to shutdown the server.
    2. Disconnects from the air.
    3. Stops the application.
    4. Tears down the run.

    Usage:
    This function should be called when the application needs to be shut down gracefully.
    It is typically called in response to a shutdown event, such as a user closing the application window.

    Returns:
    None
    """
    if app.native.main_window:
        app.native.main_window.signal_server_shutdown()
    air.disconnect()
    app.stop()
    run.tear_down()


@app.exception_handler(404)
async def _exception_handler_404(request: Request, exception: Exception) -> Response:
    """
    Handle 404 exceptions.

    This function is responsible for handling 404 exceptions that occur during request processing.
    It logs the URL that was not found, creates an error content with the provided exception,
    and builds a response with the appropriate status code.

    Parameters:
        request (Request): The request object representing the incoming request.
        exception (Exception): The exception that occurred during request processing.

    Returns:
        Response: The response object with the appropriate status code.

    Usage:
        This function is typically used as an exception handler in a web application.
        It can be registered as a handler for 404 exceptions to ensure that appropriate
        error responses are returned when a resource is not found.
    """
    log.warning(f'{request.url} not found')
    with Client(page('')) as client:
        error_content(404, exception)
    return client.build_response(request, 404)


@app.exception_handler(Exception)
async def _exception_handler_500(request: Request, exception: Exception) -> Response:
    """
    Handles exceptions that occur during the processing of a request and returns a 500 error response.

    Args:
        request (Request): The incoming request object.
        exception (Exception): The exception that occurred.

    Returns:
        Response: The response object with a 500 status code.

    Raises:
        None

    This function logs the exception, creates a client object, and builds a 500 error response.
    It is intended to be used as an exception handler for the application's request processing pipeline.

    Example usage:
        app.add_exception_handler(500, _exception_handler_500)
    """
    log.exception(exception)
    with Client(page('')) as client:
        error_content(500, exception)
    return client.build_response(request, 500)


@sio.on('handshake')
async def _on_handshake(sid: str, client_id: str) -> bool:
    """
    Handles the handshake process for a client.

    Args:
        sid (str): The session ID of the client.
        client_id (str): The ID of the client.

    Returns:
        bool: True if the handshake process is successful, False otherwise.
    """
    client = Client.instances.get(client_id)
    if not client:
        return False
    client.environ = sio.get_environ(sid)
    await sio.enter_room(sid, client.id)
    client.handle_handshake()
    return True


@sio.on('disconnect')
def _on_disconnect(sid: str) -> None:
    """
    Handle the disconnection of a client.

    This function is called when a client disconnects from the server. It retrieves the client ID from the query string
    of the disconnect request and uses it to find the corresponding client instance. If a client instance is found, the
    `handle_disconnect` method of the client is called to perform any necessary cleanup or notification.

    Parameters:
        sid (str): The session ID of the disconnected client.

    Returns:
        None
    """
    query_bytes: bytearray = sio.get_environ(sid)['asgi.scope']['query_string']
    query = urllib.parse.parse_qs(query_bytes.decode())
    client_id = query['client_id'][0]
    client = Client.instances.get(client_id)
    if client:
        client.handle_disconnect()


@sio.on('event')
def _on_event(_: str, msg: Dict) -> None:
    """
    Handle an event received from a client.

    This function is responsible for processing events received from a client and passing them to the appropriate client
    instance for further handling.

    Parameters:
        _: A string representing the event type. This parameter is ignored.
        msg: A dictionary containing the event data. It should have a 'client_id' key to identify the client.

    Returns:
        None

    Notes:
        - If the client with the given 'client_id' does not exist or does not have a socket connection, the function
          simply returns without performing any further action.
        - The 'client_id' is used to retrieve the client instance from the Client.instances dictionary.
        - The client instance's 'handle_event' method is called to process the event.
    """
    client = Client.instances.get(msg['client_id'])
    if not client or not client.has_socket_connection:
        return
    client.handle_event(msg)


@sio.on('javascript_response')
def _on_javascript_response(_: str, msg: Dict) -> None:
    """
    Handle the JavaScript response received from the client.

    This function is responsible for processing the JavaScript response received from the client.
    It retrieves the client instance based on the client ID provided in the response message.
    If the client instance is found, it calls the `handle_javascript_response` method of the client.

    Parameters:
    - _: A string representing the event name (not used in this function).
    - msg: A dictionary containing the response message from the client. It should have a 'client_id' key.

    Returns:
    None

    Usage:
    This function is typically called as a callback when a JavaScript response is received.
    It should be registered as an event handler for the corresponding event.
    """
    client = Client.instances.get(msg['client_id'])
    if not client:
        return
    client.handle_javascript_response(msg)
