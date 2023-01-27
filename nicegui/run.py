import logging
import multiprocessing
import os
import sys
import webbrowser
from typing import List, Optional

import uvicorn
from uvicorn.main import STARTUP_FAILURE
from uvicorn.supervisors import ChangeReload, Multiprocess

from . import globals


def run(*,
        host: str = '0.0.0.0',
        port: int = 8080,
        title: str = 'NiceGUI',
        viewport: str = 'width=device-width, initial-scale=1',
        favicon: Optional[str] = None,
        dark: Optional[bool] = False,
        binding_refresh_interval: float = 0.1,
        show: bool = True,
        reload: bool = True,
        uvicorn_logging_level: str = 'warning',
        uvicorn_reload_dirs: str = '.',
        uvicorn_reload_includes: str = '*.py',
        uvicorn_reload_excludes: str = '.*, .py[cod], .sw.*, ~*',
        exclude: str = '',
        tailwind: bool = True,
        ) -> None:
    '''ui.run

    You can call `ui.run()` with optional arguments:

    :param host: start server with this host (default: `'0.0.0.0'`)
    :param port: use this port (default: `8080`)
    :param title: page title (default: `'NiceGUI'`, can be overwritten per page)
    :param viewport: page meta viewport content (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)
    :param favicon: relative filepath or absolute URL to a favicon (default: `None`, NiceGUI icon will be used)
    :param dark: whether to use Quasar's dark mode (default: `False`, use `None` for "auto" mode)
    :param binding_refresh_interval: time between binding updates (default: `0.1` seconds, bigger is more CPU friendly)
    :param show: automatically open the UI in a browser tab (default: `True`)
    :param reload: automatically reload the UI on file changes (default: `True`)
    :param uvicorn_logging_level: logging level for uvicorn server (default: `'warning'`)
    :param uvicorn_reload_dirs: string with comma-separated list for directories to be monitored (default is current working directory only)
    :param uvicorn_reload_includes: string with comma-separated list of glob-patterns which trigger reload on modification (default: `'.py'`)
    :param uvicorn_reload_excludes: string with comma-separated list of glob-patterns which should be ignored for reload (default: `'.*, .py[cod], .sw.*, ~*'`)
    :param exclude: comma-separated string to exclude elements (with corresponding JavaScript libraries) to save bandwidth
      (possible entries: audio, chart, colors, interactive_image, joystick, keyboard, log, scene, table, video)
    :param tailwind: whether to use Tailwind (experimental, default: `True`)
    '''
    globals.ui_run_has_been_called = True
    globals.host = host
    globals.port = port
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
