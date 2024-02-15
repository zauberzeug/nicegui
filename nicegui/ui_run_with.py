from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional, Union

from fastapi import FastAPI

from . import core, storage
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
    mount_path: str = '/',
    tailwind: bool = True,
    prod_js: bool = True,
    storage_secret: Optional[str] = None,
) -> None:
    """Run NiceGUI with FastAPI.

    This function allows you to run NiceGUI with a FastAPI application. It sets up the necessary configurations and mounts the NiceGUI app to the specified mount path.

    - app: The FastAPI app instance.
    :type app: FastAPI
    - title: The page title. Default is 'NiceGUI'.
    :type title: str
    - viewport: The page meta viewport content. Default is 'width=device-width, initial-scale=1'.
    :type viewport: str
    - favicon: The relative filepath or absolute URL to a favicon. Default is None, which uses the NiceGUI icon. It can also be an emoji (e.g. '🚀', works for most browsers).
    :type favicon: Optional[Union[str, Path]]
    - dark: Whether to use Quasar's dark mode. Default is False. Use None for "auto" mode.
    :type dark: Optional[bool]
    - language: The language for Quasar elements. Default is 'en-US'.
    :type language: Language
    - binding_refresh_interval: The time between binding updates in seconds. Default is 0.1 seconds. A bigger value is more CPU friendly.
    :type binding_refresh_interval: float
    - reconnect_timeout: The maximum time the server waits for the browser to reconnect in seconds. Default is 3.0 seconds.
    :type reconnect_timeout: float
    - mount_path: The path at which NiceGUI should be mounted. Default is '/'.
    :type mount_path: str
    - tailwind: Whether to use Tailwind CSS. This is experimental. Default is True.
    :type tailwind: bool
    - prod_js: Whether to use the production version of Vue and Quasar dependencies. Default is True.
    :type prod_js: bool
    - storage_secret: The secret key for browser-based storage. Default is None. A value is required to enable ui.storage.individual and ui.storage.browser.
    :type storage_secret: Optional[str]
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
        tailwind=tailwind,
        prod_js=prod_js,
        show_welcome_message=False,
    )

    storage.set_storage_secret(storage_secret)

    app.mount(mount_path, core.app)
    main_app_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def lifespan_wrapper(app):
        await _startup()
        async with main_app_lifespan(app):
            yield
        await _shutdown()

    app.router.lifespan_context = lifespan_wrapper
