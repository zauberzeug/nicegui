from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal, Optional, Union

from fastapi import FastAPI

from . import core, storage
from .air import Air
from .language import Language
from .nicegui import _shutdown, _startup


def run_with(
    app: FastAPI, *,
    title: str = 'NiceGUI',
    viewport: str = 'width=device-width, initial-scale=1',
    favicon: Optional[Union[str, Path]] = None,
    dark: Optional[bool] = False,
    language: Language = 'en-US',
    binding_refresh_interval: float = 0.1,
    reconnect_timeout: float = 3.0,
    message_history_length: int = 1000,
    mount_path: str = '/',
    on_air: Optional[Union[str, Literal[True]]] = None,
    tailwind: bool = True,
    prod_js: bool = True,
    storage_secret: Optional[str] = None,
    show_welcome_message: bool = True,
) -> None:
    """Run NiceGUI with FastAPI.

    :param app: FastAPI app
    :param title: page title (default: `'NiceGUI'`, can be overwritten per page)
    :param viewport: page meta viewport content (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)
    :param favicon: relative filepath, absolute URL to a favicon (default: `None`, NiceGUI icon will be used) or emoji (e.g. `'🚀'`, works for most browsers)
    :param dark: whether to use Quasar's dark mode (default: `False`, use `None` for "auto" mode)
    :param language: language for Quasar elements (default: `'en-US'`)
    :param binding_refresh_interval: time between binding updates (default: `0.1` seconds, bigger is more CPU friendly)
    :param reconnect_timeout: maximum time the server waits for the browser to reconnect (default: 3.0 seconds)
    :param message_history_length: maximum number of messages that will be stored and resent after a connection interruption (default: 1000, use 0 to disable)
    :param mount_path: mount NiceGUI at this path (default: `'/'`)
    :param on_air: tech preview: `allows temporary remote access <https://nicegui.io/documentation/section_configuration_deployment#nicegui_on_air>`_ if set to `True` (default: disabled)
    :param tailwind: whether to use Tailwind CSS (experimental, default: `True`)
    :param prod_js: whether to use the production version of Vue and Quasar dependencies (default: `True`)
    :param storage_secret: secret key for browser-based storage (default: `None`, a value is required to enable ui.storage.individual and ui.storage.browser)
    :param show_welcome_message: whether to show the welcome message (default: `True`)
    """
    core.app.config.add_run_config(
        reload=False,
        title=title,
        viewport=viewport,
        favicon=favicon,
        dark=dark,
        language=language,
        binding_refresh_interval=binding_refresh_interval,
        reconnect_timeout=reconnect_timeout,
        message_history_length=message_history_length,
        tailwind=tailwind,
        prod_js=prod_js,
        show_welcome_message=show_welcome_message,
    )

    storage.set_storage_secret(storage_secret)

    if on_air:
        core.air = Air('' if on_air is True else on_air)

    app.mount(mount_path, core.app)
    main_app_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def lifespan_wrapper(app):
        await _startup()
        async with main_app_lifespan(app) as state:
            yield state
        await _shutdown()

    app.router.lifespan_context = lifespan_wrapper
