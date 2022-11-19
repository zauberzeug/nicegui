import inspect
import webbrowser
from typing import Optional

import uvicorn

from . import globals


def run(*,
        host: str = '0.0.0.0',
        port: int = 5000,
        title: str = 'NiceGUI',
        dark: Optional[bool] = False,
        reload: bool = True,
        binding_refresh_interval: float = 0.1,
        ) -> None:
    globals.host = host
    globals.port = port
    globals.title = title
    globals.dark = dark
    globals.binding_refresh_interval = binding_refresh_interval

    if inspect.stack()[-2].filename.endswith('spawn.py'):
        return

    webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

    uvicorn.run('nicegui:app' if reload else globals.app, host=host, port=port, reload=reload)
