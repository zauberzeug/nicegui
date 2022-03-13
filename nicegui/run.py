from typing import Awaitable, Callable, Optional, Union
import inspect
import sys
import webbrowser
import uvicorn
import os
from . import globals

if not globals.config.interactive and globals.config.reload and not inspect.stack()[-2].filename.endswith('spawn.py'):

    if globals.config.show:
        webbrowser.open(f'http://{globals.config.host}:{globals.config.port}/')
    uvicorn.run('nicegui:app', host=globals.config.host, port=globals.config.port, lifespan='on', reload=True,
                log_level=globals.config.uvicorn_logging_level)
    sys.exit()

def run(self, *,
        host: str = os.environ.get('HOST', '0.0.0.0'),
        port: int = int(os.environ.get('PORT', '8080')),
        title: str = 'NiceGUI',
        favicon: str = 'favicon.ico',
        dark: Optional[bool] = False,
        reload: bool = True,
        show: bool = True,
        on_connect: Optional[Union[Callable, Awaitable]] = None,
        uvicorn_logging_level: str = 'warning',
        main_page_classes: str = 'q-ma-md column items-start',
        binding_refresh_interval: float = 0.1,
        ):

    if globals.config.interactive or reload == False:  # NOTE: if reload == True we already started uvicorn above
        if show:
            webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')
        uvicorn.run(globals.app, host=host, port=port, lifespan='on', log_level=uvicorn_logging_level)
