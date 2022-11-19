import inspect
import webbrowser
from typing import List, Optional

import uvicorn

from . import globals


def run(*,
        host: str = '0.0.0.0',
        port: int = 8080,
        title: str = 'NiceGUI',
        dark: Optional[bool] = False,
        binding_refresh_interval: float = 0.1,
        show: bool = True,
        reload: bool = True,
        uvicorn_logging_level: str = 'warning',
        uvicorn_reload_dirs: str = '.',
        uvicorn_reload_includes: str = '*.py',
        uvicorn_reload_excludes: str = '.*, .py[cod], .sw.*, ~*',
        ) -> None:
    globals.host = host
    globals.port = port
    globals.title = title
    globals.dark = dark
    globals.binding_refresh_interval = binding_refresh_interval

    if inspect.stack()[-2].filename.endswith('spawn.py'):
        return

    if show:
        webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

    def split_args(args: str) -> List[str]:
        return args.split(',') if ',' in args else [args]

    uvicorn.run(
        'nicegui:app' if reload else globals.app,
        host=host,
        port=port,
        reload=reload,
        reload_includes=split_args(uvicorn_reload_includes) if reload else None,
        reload_excludes=split_args(uvicorn_reload_excludes) if reload else None,
        reload_dirs=split_args(uvicorn_reload_dirs) if reload else None,
        log_level=uvicorn_logging_level,
    )
