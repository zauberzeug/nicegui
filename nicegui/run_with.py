from pathlib import Path
from typing import Optional, Union

from fastapi import FastAPI

from nicegui import globals
from nicegui.helpers import set_storage_secret
from nicegui.language import Language
from nicegui.nicegui import handle_shutdown, handle_startup


def run_with(
    app: FastAPI, *,
    title: str = 'NiceGUI',
    viewport: str = 'width=device-width, initial-scale=1',
    favicon: Optional[Union[str, Path]] = None,
    dark: Optional[bool] = False,
    language: Language = 'en-US',
    binding_refresh_interval: float = 0.1,
    exclude: str = '',
    mount_path: str = '/',
    storage_secret: Optional[str] = None,
) -> None:
    globals.ui_run_has_been_called = True
    globals.title = title
    globals.viewport = viewport
    globals.favicon = favicon
    globals.dark = dark
    globals.language = language
    globals.binding_refresh_interval = binding_refresh_interval
    globals.excludes = [e.strip() for e in exclude.split(',')]
    globals.tailwind = True

    set_storage_secret(storage_secret)
    app.on_event('startup')(lambda: handle_startup(with_welcome_message=False))
    app.on_event('shutdown')(lambda: handle_shutdown())

    app.mount(mount_path, globals.app)
