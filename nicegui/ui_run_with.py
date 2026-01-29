import gc
from collections.abc import Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Literal

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from starlette.types import ASGIApp

from . import core, helpers, storage
from .air import Air
from .language import Language
from .middlewares import RedirectWithPrefixMiddleware, SetCacheControlMiddleware
from .nicegui import _shutdown, _startup
from .server import Server


def run_with(
    app: FastAPI, *,
    root: Callable | None = None,
    title: str = 'NiceGUI',
    viewport: str = 'width=device-width, initial-scale=1',
    favicon: str | Path | None = None,
    dark: bool | None = False,
    language: Language = 'en-US',
    binding_refresh_interval: float | None = 0.1,
    reconnect_timeout: float = 3.0,
    message_history_length: int = 1000,
    cache_control_directives: str = 'public, max-age=31536000, immutable, stale-while-revalidate=31536000',
    gzip_middleware_factory: Callable[[ASGIApp], GZipMiddleware] | None = GZipMiddleware,
    mount_path: str = '/',
    on_air: str | Literal[True] | None = None,
    tailwind: bool = True,
    unocss: Literal['mini', 'wind3', 'wind4'] | None = None,
    prod_js: bool = True,
    storage_secret: str | None = None,
    session_middleware_kwargs: dict[str, Any] | None = None,
    show_welcome_message: bool = True,
) -> None:
    """Run NiceGUI with FastAPI.

    :param app: FastAPI app
    :param root: root page function (*added in version 3.0.0*)
    :param title: page title (default: `'NiceGUI'`, can be overwritten per page)
    :param viewport: page meta viewport content (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)
    :param favicon: relative filepath, absolute URL to a favicon (default: `None`, NiceGUI icon will be used) or emoji (e.g. `'🚀'`, works for most browsers)
    :param dark: whether to use Quasar's dark mode (default: `False`, use `None` for "auto" mode)
    :param language: language for Quasar elements (default: `'en-US'`)
    :param binding_refresh_interval: interval for updating active links (default: 0.1 seconds, bigger is more CPU friendly, *since version 3.4.0*: can be ``None`` to disable update loop)
    :param reconnect_timeout: maximum time the server waits for the browser to reconnect (default: 3.0 seconds)
    :param message_history_length: maximum number of messages that will be stored and resent after a connection interruption (default: 1000, use 0 to disable, *added in version 2.9.0*)
    :param cache_control_directives: cache control directives for internal static files (default: `'public, max-age=31536000, immutable, stale-while-revalidate=31536000'`)
    :param gzip_middleware_factory: GZipMiddleware factory function (e.g. ``lambda app: GZipMiddleware(app, minimum_size=500, compresslevel=9)``, defaults to Starlette's ``GZipMiddleware``, can be ``None`` to disable, *added in version 3.5.0*)
    :param mount_path: mount NiceGUI at this path (default: `'/'`)
    :param on_air: tech preview: `allows temporary remote access <https://nicegui.io/documentation/section_configuration_deployment#nicegui_on_air>`_ if set to `True` (default: disabled)
    :param tailwind: whether to use Tailwind CSS (experimental, default: `True`)
    :param unocss: use UnoCSS with the specified preset instead of Tailwind CSS (default: ``None``, options: "mini", "wind3", "wind4", *added in version 3.7.0*)
    :param prod_js: whether to use the production version of Vue and Quasar dependencies (default: `True`)
    :param storage_secret: secret key for browser-based storage (default: `None`, a value is required to enable ui.storage.individual and ui.storage.browser)
    :param session_middleware_kwargs: additional keyword arguments passed to SessionMiddleware that creates the session cookies used for browser-based storage
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
        unocss=unocss,
        prod_js=prod_js,
        show_welcome_message=show_welcome_message,
        cache_control_directives=cache_control_directives,
    )
    core.root = root
    storage.set_storage_secret(storage_secret, session_middleware_kwargs)
    if not helpers.is_pytest() and gzip_middleware_factory is not None:
        core.app.add_middleware(gzip_middleware_factory)
    core.app.add_middleware(RedirectWithPrefixMiddleware)
    core.app.add_middleware(SetCacheControlMiddleware)

    if on_air:
        core.air = Air('' if on_air is True else on_air)

    app.mount(mount_path, core.app)
    main_app_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def lifespan_wrapper(app):
        def _get_server_instance() -> uvicorn.Server | None:
            for server in (obj for obj in gc.get_objects() if isinstance(obj, uvicorn.Server)):
                wrapped = server.config.loaded_app
                while wrapped is not None:
                    if wrapped is app:
                        return server
                    wrapped = getattr(wrapped, 'app', None)
            return None
        if (instance := _get_server_instance()) is not None:
            Server.instance = instance
        await _startup()
        async with main_app_lifespan(app) as state:
            yield state
        await _shutdown()

    app.router.lifespan_context = lifespan_wrapper
