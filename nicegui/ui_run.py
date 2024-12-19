import multiprocessing
import os
import sys
from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple, TypedDict, Union

from starlette.routing import Route
from uvicorn.main import STARTUP_FAILURE
from uvicorn.supervisors import ChangeReload, Multiprocess

import __main__

from . import core, helpers
from . import native as native_module
from .air import Air
from .client import Client
from .language import Language
from .logging import log
from .server import CustomServerConfig, Server

APP_IMPORT_STRING = 'nicegui:app'


class ContactDict(TypedDict):
    name: Optional[str]
    url: Optional[str]
    email: Optional[str]


class LicenseInfoDict(TypedDict):
    name: str
    identifier: Optional[str]
    url: Optional[str]


class DocsConfig(TypedDict):
    title: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    version: Optional[str]
    terms_of_service: Optional[str]
    contact: Optional[ContactDict]
    license_info: Optional[LicenseInfoDict]


def run(*,
        host: Optional[str] = None,
        port: Optional[int] = None,
        title: str = 'NiceGUI',
        viewport: str = 'width=device-width, initial-scale=1',
        favicon: Optional[Union[str, Path]] = None,
        dark: Optional[bool] = False,
        language: Language = 'en-US',
        binding_refresh_interval: float = 0.1,
        reconnect_timeout: float = 3.0,
        message_history_length: int = 1000,
        fastapi_docs: Union[bool, DocsConfig] = False,
        show: bool = True,
        on_air: Optional[Union[str, Literal[True]]] = None,
        native: bool = False,
        window_size: Optional[Tuple[int, int]] = None,
        fullscreen: bool = False,
        frameless: bool = False,
        reload: bool = True,
        uvicorn_logging_level: str = 'warning',
        uvicorn_reload_dirs: str = '.',
        uvicorn_reload_includes: str = '*.py',
        uvicorn_reload_excludes: str = '.*, .py[cod], .sw.*, ~*',
        tailwind: bool = True,
        prod_js: bool = True,
        endpoint_documentation: Literal['none', 'internal', 'page', 'all'] = 'none',
        storage_secret: Optional[str] = None,
        show_welcome_message: bool = True,
        **kwargs: Any,
        ) -> None:
    """ui.run

    You can call `ui.run()` with optional arguments.
    Most of them only apply after stopping and fully restarting the app and do not apply with auto-reloading.

    :param host: start server with this host (defaults to `'127.0.0.1` in native mode, otherwise `'0.0.0.0'`)
    :param port: use this port (default: 8080 in normal mode, and an automatically determined open port in native mode)
    :param title: page title (default: `'NiceGUI'`, can be overwritten per page)
    :param viewport: page meta viewport content (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)
    :param favicon: relative filepath, absolute URL to a favicon (default: `None`, NiceGUI icon will be used) or emoji (e.g. `'🚀'`, works for most browsers)
    :param dark: whether to use Quasar's dark mode (default: `False`, use `None` for "auto" mode)
    :param language: language for Quasar elements (default: `'en-US'`)
    :param binding_refresh_interval: time between binding updates (default: `0.1` seconds, bigger is more CPU friendly)
    :param reconnect_timeout: maximum time the server waits for the browser to reconnect (default: 3.0 seconds)
    :param message_history_length: maximum number of messages that will be stored and resent after a connection interruption (default: 1000, use 0 to disable)
    :param fastapi_docs: enable FastAPI's automatic documentation with Swagger UI, ReDoc, and OpenAPI JSON (bool or dictionary as described `here<https://fastapi.tiangolo.com/tutorial/metadata/>`_, default: `False`)
    :param show: automatically open the UI in a browser tab (default: `True`)
    :param on_air: tech preview: `allows temporary remote access <https://nicegui.io/documentation/section_configuration_deployment#nicegui_on_air>`_ if set to `True` (default: disabled)
    :param native: open the UI in a native window of size 800x600 (default: `False`, deactivates `show`, automatically finds an open port)
    :param window_size: open the UI in a native window with the provided size (e.g. `(1024, 786)`, default: `None`, also activates `native`)
    :param fullscreen: open the UI in a fullscreen window (default: `False`, also activates `native`)
    :param frameless: open the UI in a frameless window (default: `False`, also activates `native`)
    :param reload: automatically reload the UI on file changes (default: `True`)
    :param uvicorn_logging_level: logging level for uvicorn server (default: `'warning'`)
    :param uvicorn_reload_dirs: string with comma-separated list for directories to be monitored (default is current working directory only)
    :param uvicorn_reload_includes: string with comma-separated list of glob-patterns which trigger reload on modification (default: `'*.py'`)
    :param uvicorn_reload_excludes: string with comma-separated list of glob-patterns which should be ignored for reload (default: `'.*, .py[cod], .sw.*, ~*'`)
    :param tailwind: whether to use Tailwind (experimental, default: `True`)
    :param prod_js: whether to use the production version of Vue and Quasar dependencies (default: `True`)
    :param endpoint_documentation: control what endpoints appear in the autogenerated OpenAPI docs (default: 'none', options: 'none', 'internal', 'page', 'all')
    :param storage_secret: secret key for browser-based storage (default: `None`, a value is required to enable ui.storage.individual and ui.storage.browser)
    :param show_welcome_message: whether to show the welcome message (default: `True`)
    :param kwargs: additional keyword arguments are passed to `uvicorn.run`
    """
    core.app.config.add_run_config(
        reload=reload,
        title=title,
        viewport=viewport,
        favicon=favicon,
        dark=dark,
        language=language,
        binding_refresh_interval=binding_refresh_interval,
        reconnect_timeout=reconnect_timeout,
        message_history_length=message_history_length,
        tailwind=tailwind,
        prod_js=prod_js,
        show_welcome_message=show_welcome_message,
    )
    core.app.config.endpoint_documentation = endpoint_documentation

    for route in core.app.routes:
        if not isinstance(route, Route):
            continue
        if route.path.startswith('/_nicegui') and hasattr(route, 'methods'):
            route.include_in_schema = endpoint_documentation in {'internal', 'all'}
        if route.path == '/' or route.path in Client.page_routes.values():
            route.include_in_schema = endpoint_documentation in {'page', 'all'}

    if fastapi_docs:
        if not core.app.docs_url:
            core.app.docs_url = '/docs'
        if not core.app.redoc_url:
            core.app.redoc_url = '/redoc'
        if not core.app.openapi_url:
            core.app.openapi_url = '/openapi.json'
        if isinstance(fastapi_docs, dict):
            core.app.title = fastapi_docs.get('title') or title
            core.app.summary = fastapi_docs.get('summary')
            core.app.description = fastapi_docs.get('description') or ''
            core.app.version = fastapi_docs.get('version') or '0.1.0'
            core.app.terms_of_service = fastapi_docs.get('terms_of_service')
            contact = fastapi_docs.get('contact')
            license_info = fastapi_docs.get('license_info')
            core.app.contact = dict(contact) if contact else None
            core.app.license_info = dict(license_info) if license_info else None
        core.app.setup()

    if on_air:
        core.air = Air('' if on_air is True else on_air)

    if multiprocessing.current_process().name != 'MainProcess':
        return

    if reload and not hasattr(__main__, '__file__'):
        log.warning('disabling auto-reloading because is is only supported when running from a file')
        core.app.config.reload = reload = False

    if fullscreen:
        native = True
    if frameless:
        native = True
    if window_size:
        native = True
    if native:
        show = False
        host = host or '127.0.0.1'
        port = port or native_module.find_open_port()
        width, height = window_size or (800, 600)
        native_module.activate(host, port, title, width, height, fullscreen, frameless)
    else:
        port = port or 8080
        host = host or '0.0.0.0'
    assert host is not None
    assert port is not None

    # NOTE: We save host and port in environment variables so the subprocess started in reload mode can access them.
    os.environ['NICEGUI_HOST'] = host
    os.environ['NICEGUI_PORT'] = str(port)

    if show:
        helpers.schedule_browser(host, port)

    def split_args(args: str) -> List[str]:
        return [a.strip() for a in args.split(',')]

    if kwargs.get('workers', 1) > 1:
        raise ValueError('NiceGUI does not support multiple workers yet.')

    # NOTE: The following lines are basically a copy of `uvicorn.run`, but keep a reference to the `server`.

    config = CustomServerConfig(
        APP_IMPORT_STRING if reload else core.app,
        host=host,
        port=port,
        reload=reload,
        reload_includes=split_args(uvicorn_reload_includes) if reload else None,
        reload_excludes=split_args(uvicorn_reload_excludes) if reload else None,
        reload_dirs=split_args(uvicorn_reload_dirs) if reload else None,
        log_level=uvicorn_logging_level,
        **kwargs,
    )
    config.storage_secret = storage_secret
    config.method_queue = native_module.method_queue if native else None
    config.response_queue = native_module.response_queue if native else None
    Server.create_singleton(config)

    if (reload or config.workers > 1) and not isinstance(config.app, str):
        log.warning('You must pass the application as an import string to enable "reload" or "workers".')
        sys.exit(1)

    if config.should_reload:
        sock = config.bind_socket()
        ChangeReload(config, target=Server.instance.run, sockets=[sock]).run()
    elif config.workers > 1:
        sock = config.bind_socket()
        Multiprocess(config, target=Server.instance.run, sockets=[sock]).run()
    else:
        Server.instance.run()
    if config.uds:
        os.remove(config.uds)  # pragma: py-win32

    if not Server.instance.started and not config.should_reload and config.workers == 1:
        sys.exit(STARTUP_FAILURE)
