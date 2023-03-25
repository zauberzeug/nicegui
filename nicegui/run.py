import logging
import multiprocessing
import os
import sys
import webbrowser
from typing import List, Optional, Tuple

import uvicorn
from uvicorn.main import STARTUP_FAILURE
from uvicorn.supervisors import ChangeReload, Multiprocess

from . import globals, native_mode


def run(*,
        host: Optional[str] = None,
        port: int = 8080,
        title: str = 'NiceGUI',
        viewport: str = 'width=device-width, initial-scale=1',
        favicon: Optional[str] = None,
        dark: Optional[bool] = False,
        binding_refresh_interval: float = 0.1,
        show: bool = True,
        native: bool = False,
        window_size: Optional[Tuple[int, int]] = None,
        fullscreen: bool = False,
        reload: bool = True,
        uvicorn_logging_level: str = 'warning',
        uvicorn_reload_dirs: str = '.',
        uvicorn_reload_includes: str = '*.py',
        uvicorn_reload_excludes: str = '.*, .py[cod], .sw.*, ~*',
        exclude: str = '',
        tailwind: bool = True,
        icon_dir = None,
        **kwargs,
        ) -> None:
    '''ui.run

    You can call `ui.run()` with optional arguments:

    :param host: start server with this host (defaults to `'127.0.0.1` in native mode, otherwise `'0.0.0.0'`)
    :param port: use this port (default: `8080`)
    :param title: page title (default: `'NiceGUI'`, can be overwritten per page)
    :param viewport: page meta viewport content (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)
    :param favicon: relative filepath or absolute URL to a favicon (default: `None`, NiceGUI icon will be used)
    :param dark: whether to use Quasar's dark mode (default: `False`, use `None` for "auto" mode)
    :param binding_refresh_interval: time between binding updates (default: `0.1` seconds, bigger is more CPU friendly)
    :param show: automatically open the UI in a browser tab (default: `True`)
    :param native: open the UI in a native window of size 800x600 (default: `False`, deactivates `show`, automatically finds an open port)
    :param window_size: open the UI in a native window with the provided size (e.g. `(1024, 786)`, default: `None`, also activates `native`)
    :param fullscreen: open the UI in a fullscreen window (default: `False`, also activates `native`)
    :param reload: automatically reload the UI on file changes (default: `True`)
    :param uvicorn_logging_level: logging level for uvicorn server (default: `'warning'`)
    :param uvicorn_reload_dirs: string with comma-separated list for directories to be monitored (default is current working directory only)
    :param uvicorn_reload_includes: string with comma-separated list of glob-patterns which trigger reload on modification (default: `'.py'`)
    :param uvicorn_reload_excludes: string with comma-separated list of glob-patterns which should be ignored for reload (default: `'.*, .py[cod], .sw.*, ~*'`)
    :param exclude: comma-separated string to exclude elements (with corresponding JavaScript libraries) to save bandwidth
      (possible entries: aggrid, audio, chart, colors, interactive_image, joystick, keyboard, log, markdown, mermaid, plotly, scene, video)
    :param tailwind: whether to use Tailwind (experimental, default: `True`)
    :param kwargs: additional keyword arguments are passed to `uvicorn.run`
    '''
    globals.ui_run_has_been_called = True
    globals.reload = reload
    globals.title = title
    globals.viewport = viewport
    globals.favicon = favicon
    globals.dark = dark
    globals.binding_refresh_interval = binding_refresh_interval
    globals.excludes = [e.strip() for e in exclude.split(',')]
    globals.tailwind = tailwind

    if multiprocessing.current_process().name != 'MainProcess':
        return

    if fullscreen:
        native = True
    if window_size:
        native = True
    if native:
        show = False
        host = host or '127.0.0.1'
        port = native_mode.find_open_port()
        width, height = window_size or (800, 600)
        native_mode.activate(f'http://{host}:{port}', title, width, height, fullscreen, icon_dir)
    else:
        host = host or '0.0.0.0'

    # NOTE: We save the URL in an environment variable so the subprocess started in reload mode can access it.
    os.environ['NICEGUI_URL'] = f'http://{host}:{port}'

    if show:
        webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

    def split_args(args: str) -> List[str]:
        return [a.strip() for a in args.split(',')]

    # NOTE: The following lines are basically a copy of `uvicorn.run`, but keep a reference to the `server`.

    config = uvicorn.Config(
        'nicegui:app' if reload else globals.app,
        host=host,
        port=port,
        reload=reload,
        reload_includes=split_args(uvicorn_reload_includes) if reload else None,
        reload_excludes=split_args(uvicorn_reload_excludes) if reload else None,
        reload_dirs=split_args(uvicorn_reload_dirs) if reload else None,
        log_level=uvicorn_logging_level,
        **kwargs,
    )
    globals.server = uvicorn.Server(config=config)

    if (reload or config.workers > 1) and not isinstance(config.app, str):
        logging.warning('You must pass the application as an import string to enable "reload" or "workers".')
        sys.exit(1)

    if config.should_reload:
        sock = config.bind_socket()
        ChangeReload(config, target=globals.server.run, sockets=[sock]).run()
    elif config.workers > 1:
        sock = config.bind_socket()
        Multiprocess(config, target=globals.server.run, sockets=[sock]).run()
    else:
        globals.server.run()
    if config.uds:
        os.remove(config.uds)  # pragma: py-win32

    if not globals.server.started and not config.should_reload and config.workers == 1:
        sys.exit(STARTUP_FAILURE)
