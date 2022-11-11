import inspect
import webbrowser

import uvicorn

from . import globals


def run(*,
        host: str = '0.0.0.0',
        port: int = 5000,
        reload: bool = True,
        binding_refresh_interval: float = 0.1,
        ) -> None:
    globals.host = host
    globals.port = port
    globals.binding_refresh_interval = binding_refresh_interval

    if inspect.stack()[-2].filename.endswith('spawn.py'):
        return

    webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

    uvicorn.run('nicegui:app' if reload else globals.app, host=host, port=port, reload=reload)
