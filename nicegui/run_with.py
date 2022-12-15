from typing import Optional

from fastapi import FastAPI

from nicegui import globals
from nicegui.nicegui import handle_shutdown, handle_startup


def run_with(
    app: FastAPI, *,
    title: str = 'NiceGUI',
    favicon: Optional[str] = None,
    dark: Optional[bool] = False,
    binding_refresh_interval: float = 0.1,
    exclude: str = '',
) -> None:
    globals.title = title
    globals.favicon = favicon
    globals.dark = dark
    globals.binding_refresh_interval = binding_refresh_interval
    globals.excludes = [e.strip() for e in exclude.split(',')]

    app.on_event('startup')(lambda: handle_startup(with_welcome_message=False))
    app.on_event('shutdown')(lambda: handle_shutdown())

    app.mount('/', globals.app)
