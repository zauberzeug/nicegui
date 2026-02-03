import multiprocessing
import os
import runpy
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal, TypedDict

from fastapi.middleware.gzip import GZipMiddleware
from starlette.routing import Route
from starlette.types import ASGIApp
from uvicorn.main import STARTUP_FAILURE
from uvicorn.supervisors import ChangeReload, Multiprocess

from . import core, helpers
from . import native as native_module
from .air import Air
from .client import Client
from .language import Language
from .logging import log
from .middlewares import RedirectWithPrefixMiddleware, SetCacheControlMiddleware
from .server import CustomServerConfig, Server
from .storage import set_storage_secret

APP_IMPORT_STRING = 'nicegui:app'


class ContactDict(TypedDict):
    name: str | None
    url: str | None
    email: str | None


class LicenseInfoDict(TypedDict):
    name: str
    identifier: str | None
    url: str | None


class DocsConfig(TypedDict):
    title: str | None
    summary: str | None
    description: str | None
    version: str | None
    terms_of_service: str | None
    contact: ContactDict | None
    license_info: LicenseInfoDict | None


def run(root: Callable | None = None, *,
        host: str | None = None,
        port: int | None = None,
        title: str = 'NiceGUI',
        viewport: str = 'width=device-width, initial-scale=1',
        favicon: str | Path | None = None,
        dark: bool | None = False,
        language: Language = 'en-US',
        binding_refresh_interval: float | None = 0.1,
        reconnect_timeout: float = 3.0,
        message_history_length: int = 1000,
        cache_control_directives: str = 'public, max-age=31536000, immutable, stale-while-revalidate=31536000',
        gzip_middleware_factory: Callable[[ASGIApp], GZipMiddleware] | None = GZipMiddleware,
        fastapi_docs: bool | DocsConfig = False,
        show: bool | str = True,
        on_air: str | Literal[True] | None = None,
        native: bool = False,
        window_size: tuple[int, int] | None = None,
        fullscreen: bool = False,
        frameless: bool = False,
        reload: bool = True,
        uvicorn_logging_level: str = 'warning',
        uvicorn_reload_dirs: str = '.',
        uvicorn_reload_includes: str = '*.py',
        uvicorn_reload_excludes: str = '.*, .py[cod], .sw.*, ~*',
        tailwind: bool = True,
        unocss: Literal['mini', 'wind3', 'wind4'] | None = None,
        prod_js: bool = True,
        endpoint_documentation: Literal['none', 'internal', 'page', 'all'] = 'none',
        storage_secret: str | None = None,
        session_middleware_kwargs: dict[str, Any] | None = None,
        show_welcome_message: bool = True,
        **kwargs: Any,
        ) -> None:
    """ui.run

    You can call `ui.run()` with optional arguments.
    Most of them only apply after stopping and fully restarting the app and do not apply with auto-reloading.

    :param root: root page function (*added in version 3.0.0*)
    :param host: start server with this host (defaults to `'127.0.0.1` in native mode, otherwise `'0.0.0.0'`)
    :param port: use this port (default: 8080 in normal mode, and an automatically determined open port in native mode)
    :param title: page title (default: `'NiceGUI'`, can be overwritten per page)
    :param viewport: page meta viewport content (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)
    :param favicon: relative filepath, absolute URL to a favicon (default: `None`, NiceGUI icon will be used) or emoji (e.g. `'🚀'`, works for most browsers)
    :param dark: whether to use Quasar's dark mode (default: `False`, use `None` for "auto" mode)
    :param language: language for Quasar elements (default: `'en-US'`)
    :param binding_refresh_interval: interval for updating active links (default: 0.1 seconds, bigger is more CPU friendly, *since version 3.4.0*: can be ``None`` to disable update loop)
    :param reconnect_timeout: maximum time the server waits for the browser to reconnect (default: 3.0 seconds)
    :param message_history_length: maximum number of messages that will be stored and resent after a connection interruption (default: 1000, use 0 to disable, *added in version 2.9.0*)
    :param cache_control_directives: cache control directives for internal static files (default: `'public, max-age=31536000, immutable, stale-while-revalidate=31536000'`)
    :param gzip_middleware_factory: GZipMiddleware factory function (e.g. ``lambda app: GZipMiddleware(app, minimum_size=500, compresslevel=9)``, defaults to Starlette's ``GZipMiddleware``, can be ``None`` to disable, *added in version 3.5.0*)
    :param fastapi_docs: enable FastAPI's automatic documentation with Swagger UI, ReDoc, and OpenAPI JSON (bool or dictionary as described `here <https://fastapi.tiangolo.com/tutorial/metadata/>`_, default: `False`, *updated in version 2.9.0*)
    :param show: automatically open the UI in a browser tab (default: `True`, opens "/", *since version 3.6.0*: you can pass a specific path like "/path/to/page")
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
    :param tailwind: whether to use Tailwind CSS (experimental, default: `True`)
    :param unocss: use UnoCSS with the specified preset instead of Tailwind CSS (default: ``None``, options: "mini", "wind3", "wind4", *added in version 3.7.0*)
    :param prod_js: whether to use the production version of Vue and Quasar dependencies (default: `True`)
    :param endpoint_documentation: control what endpoints appear in the autogenerated OpenAPI docs (default: 'none', options: 'none', 'internal', 'page', 'all')
    :param storage_secret: secret key for browser-based storage (default: `None`, a value is required to enable ui.storage.individual and ui.storage.browser)
    :param session_middleware_kwargs: additional keyword arguments passed to SessionMiddleware that creates the session cookies used for browser-based storage
    :param show_welcome_message: whether to show the welcome message (default: `True`)
    :param kwargs: additional keyword arguments are passed to `uvicorn.run`
    """
    if core.script_mode:
        if Client.page_routes:
            if core.script_client and not core.script_client.content.default_slot.children and (
                core.script_client._head_html or core.script_client._body_html  # pylint: disable=protected-access
            ):
                raise RuntimeError(
                    'ui.add_head_html, ui.add_body_html, or ui.add_css has been called inside the global scope while using ui.page.\n'
                    'Consider using shared=True for this call to add the code to all pages.\n'
                    'Alternatively, to add the code to a specific page, move the call into the page function.'
                )
            raise RuntimeError(
                'ui.page cannot be used in NiceGUI scripts when UI is defined in the global scope.\n'
                'To use multiple pages, either move all UI into page functions or use ui.sub_pages.'
            )

        if helpers.is_pytest():
            raise RuntimeError('Script mode is not supported in pytest. '
                               'Please pass a root function to ui.run() or use page decorators.')
        if core.app.is_started:
            return

        def run_script() -> None:
            if not sys.argv or not sys.argv[0] or not helpers.is_file(sys.argv[0]):
                raise RuntimeError(
                    'Script mode requires a valid script file to re-execute.\n'
                    'This error occurs when running code interactively (e.g., Shift-Enter in an IDE).\n'
                    'To fix this, either:\n'
                    '  1. Run the complete file instead of a selection (e.g., "python script.py")\n'
                    '  2. Use a root function: wrap your UI code in a function and pass it to ui.run(root=my_function)'
                )
            runpy.run_path(sys.argv[0], run_name='__main__')
        root = run_script
        assert core.script_client is not None
        core.script_client.delete()

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
        cache_control_directives=cache_control_directives,
        tailwind=tailwind,
        unocss=unocss,
        prod_js=prod_js,
        show_welcome_message=show_welcome_message,
    )
    core.root = root
    core.app.config.endpoint_documentation = endpoint_documentation
    if not helpers.is_pytest() and gzip_middleware_factory is not None:
        core.app.add_middleware(gzip_middleware_factory)
    core.app.add_middleware(RedirectWithPrefixMiddleware)
    core.app.add_middleware(SetCacheControlMiddleware)

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

    if helpers.is_user_simulation():
        set_storage_secret(storage_secret, session_middleware_kwargs)
        return

    if on_air:
        core.air = Air('' if on_air is True else on_air)

    if multiprocessing.current_process().name != 'MainProcess':
        return

    is_repl = bool(getattr(sys, 'ps1', sys.flags.interactive))
    if reload and is_repl:
        log.warning('disabling auto-reloading because it is only supported when running from a file')
        core.app.config.reload = reload = False

    if kwargs.get('ssl_certfile') and kwargs.get('ssl_keyfile'):
        protocol = 'https'
    else:
        protocol = 'http'

    if fullscreen:
        native = True
    if frameless:
        native = True
    if window_size:
        native = True
    shutdown_event = None
    if native:
        show = False
        host = host or '127.0.0.1'
        port = port or native_module.find_open_port()
        width, height = window_size or (800, 600)
        native_host = '127.0.0.1' if host == '0.0.0.0' else host
        if reload:
            shutdown_event = multiprocessing.Event()
        native_module.activate(protocol, native_host, port, title, width, height, fullscreen, frameless, shutdown_event)
    else:
        port = port or 8080
        host = host or '0.0.0.0'
    assert host is not None
    assert port is not None

    if helpers.is_pytest():
        port = int(os.environ['NICEGUI_SCREEN_TEST_PORT'])
        show = False
        reload = False
        native = False
        show_welcome_message = False

    # NOTE: We save host and port in environment variables so the subprocess started in reload mode can access them.
    os.environ['NICEGUI_HOST'] = host
    os.environ['NICEGUI_PORT'] = str(port)
    os.environ['NICEGUI_PROTOCOL'] = protocol

    if show:
        helpers.schedule_browser(protocol, host, port, show if isinstance(show, str) else '/')

    def split_args(args: str) -> list[str]:
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
        ws='wsproto',
        **kwargs,
    )
    config.storage_secret = storage_secret
    config.method_queue = native_module.native.method_queue if native else None
    config.response_queue = native_module.native.response_queue if native else None
    config.shutdown_event = shutdown_event
    config.session_middleware_kwargs = session_middleware_kwargs
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
