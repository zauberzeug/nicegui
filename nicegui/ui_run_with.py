from pathlib import Path
from typing import Optional, Union

from fastapi import FastAPI

from . import core, storage
from .language import Language


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

    :param app: FastAPI app
    :param title: page title (default: `'NiceGUI'`, can be overwritten per page)
    :param viewport: page meta viewport content (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)
    :param favicon: relative filepath, absolute URL to a favicon (default: `None`, NiceGUI icon will be used) or emoji (e.g. `'🚀'`, works for most browsers)
    :param dark: whether to use Quasar's dark mode (default: `False`, use `None` for "auto" mode)
    :param language: language for Quasar elements (default: `'en-US'`)
    :param binding_refresh_interval: time between binding updates (default: `0.1` seconds, bigger is more CPU friendly)
    :param reconnect_timeout: maximum time the server waits for the browser to reconnect (default: 3.0 seconds)
    :param mount_path: mount NiceGUI at this path (default: `'/'`)
    :param tailwind: whether to use Tailwind CSS (experimental, default: `True`)
    :param prod_js: whether to use the production version of Vue and Quasar dependencies (default: `True`)
    :param storage_secret: secret key for browser-based storage (default: `None`, a value is required to enable ui.storage.individual and ui.storage.browser)
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
    )

    storage.set_storage_secret(storage_secret)

    app.mount(mount_path, core.app)
