import inspect
import logging
import os
import sys
import webbrowser
from typing import List, Optional

import uvicorn
from uvicorn.main import STARTUP_FAILURE
from uvicorn.supervisors import ChangeReload, Multiprocess

from . import globals
from .config import Config


def _start_server(config: Config) -> None:
    if config.show:
        webbrowser.open(f'http://{config.host if config.host != "0.0.0.0" else "127.0.0.1"}:{config.port}/')

    def split_args(args: str) -> List[str]:
        return args.split(',') if ',' in args else [args]

    config = uvicorn.Config(
        'nicegui:app' if config.reload else globals.app,
        host=config.host,
        port=config.port,
        lifespan='on',
        reload=config.reload,
        reload_includes=split_args(config.uvicorn_reload_includes) if config.reload else None,
        reload_excludes=split_args(config.uvicorn_reload_excludes) if config.reload else None,
        reload_dirs=split_args(config.uvicorn_reload_dirs) if config.reload else None,
        log_level=config.uvicorn_logging_level,
    )
    globals.server = uvicorn.Server(config=config)

    if (config.reload or config.workers > 1) and not isinstance(config.app, str):
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


if globals.pre_evaluation_succeeded and globals.config.reload and not inspect.stack()[-2].filename.endswith('spawn.py'):
    _start_server(globals.config)
    sys.exit()


def run(self, *,
        host: str = os.environ.get('HOST', '0.0.0.0'),
        port: int = int(os.environ.get('PORT', '8080')),
        title: str = 'NiceGUI',
        favicon: str = 'favicon.ico',
        dark: Optional[bool] = False,
        reload: bool = True,
        show: bool = True,
        uvicorn_logging_level: str = 'warning',
        uvicorn_reload_dirs: str = '.',
        uvicorn_reload_includes: str = '*.py',
        uvicorn_reload_excludes: str = '.*, .py[cod], .sw.*, ~*',
        main_page_classes: str = 'q-ma-md column items-start',
        binding_refresh_interval: float = 0.1,
        exclude: str = '',
        ):
    if globals.pre_evaluation_succeeded and globals.config.reload == True:
        return  # server has already started after pre-evaluating ui.run()

    globals.config.host = host
    globals.config.port = port
    globals.config.title = title
    globals.config.favicon = favicon
    globals.config.dark = dark
    globals.config.reload = reload
    globals.config.show = show
    globals.config.uvicorn_logging_level = uvicorn_logging_level
    globals.config.uvicorn_reload_dirs = uvicorn_reload_dirs
    globals.config.uvicorn_reload_includes = uvicorn_reload_includes
    globals.config.uvicorn_reload_excludes = uvicorn_reload_excludes
    globals.config.main_page_classes = main_page_classes
    globals.config.binding_refresh_interval = binding_refresh_interval

    main_page = globals.page_stack[-1]
    main_page.title = globals.config.title
    main_page.favicon = globals.config.favicon
    main_page.dark = globals.config.dark
    main_page.view.classes = globals.config.main_page_classes

    if inspect.stack()[-2].filename.endswith('spawn.py'):
        return  # server is reloading

    if not globals.pre_evaluation_succeeded:
        if exclude or reload:
            logging.warning('Failed to pre-evaluate ui.run().')
        if exclude:
            logging.warning('The `exclude` argument will be ignored.')
        if reload:
            logging.warning('Reloading main script...')

    _start_server(globals.config)
