import inspect
import os
import sys
import webbrowser
from typing import Optional

import uvicorn

from . import globals

if not globals.config.interactive and globals.config.reload and not inspect.stack()[-2].filename.endswith('spawn.py'):

    if globals.config.show:
        webbrowser.open(f'http://{globals.config.host}:{globals.config.port}/')
    uvicorn.run(
        'nicegui:app',
        host=globals.config.host,
        port=globals.config.port,
        lifespan='on',
        reload=True,
        reload_includes=globals.config.uvicorn_reload_includes,
        reload_excludes=globals.config.uvicorn_reload_excludes,
        reload_dirs=globals.config.uvicorn_reload_dirs,
        log_level=globals.config.uvicorn_logging_level,
    )
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
    if globals.config.interactive:
        print('Error: Unexpected ui.run() in interactive mode.', flush=True)
        sys.exit()

    if globals.config.interactive or reload == False:  # NOTE: if reload == True we already started uvicorn above
        if show:
            webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')
        uvicorn.run(globals.app, host=host, port=port, lifespan='on', log_level=uvicorn_logging_level)
