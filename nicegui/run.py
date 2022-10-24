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

os.environ['STATIC_DIRECTORY'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
os.environ['TEMPLATES_DIRECTORY'] = os.path.join(os.environ['STATIC_DIRECTORY'], 'templates')


def run(self, *,
        host: str = os.environ.get('HOST', '0.0.0.0'),
        port: int = int(os.environ.get('PORT', '8080')),
        title: str = 'NiceGUI',
        favicon: Optional[str] = None,
        dark: Optional[bool] = False,
        main_page_classes: str = 'q-pa-md column items-start gap-4',
        binding_refresh_interval: float = 0.1,
        show: bool = True,
        reload: bool = True,
        uvicorn_logging_level: str = 'warning',
        uvicorn_reload_dirs: str = '.',
        uvicorn_reload_includes: str = '*.py',
        uvicorn_reload_excludes: str = '.*, .py[cod], .sw.*, ~*',
        exclude: str = '',
        ):
    globals.config = Config(
        host=host,
        port=port,
        title=title,
        reload=reload,
        favicon=favicon,
        dark=dark,
        main_page_classes=main_page_classes,
        binding_refresh_interval=binding_refresh_interval,
        excludes=[e.strip() for e in exclude.split(',')],
    )
    os.environ['HOST'] = globals.config.host
    os.environ['PORT'] = str(globals.config.port)

    if inspect.stack()[-2].filename.endswith('spawn.py'):
        return

    if show:
        webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

    def split_args(args: str) -> List[str]:
        return args.split(',') if ',' in args else [args]

    # NOTE: The following lines are basically a copy of `uvicorn.run`, but keep a reference to the `server`.

    config = uvicorn.Config(
        'nicegui:app' if reload else globals.app,
        host=host,
        port=port,
        lifespan='on',
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
