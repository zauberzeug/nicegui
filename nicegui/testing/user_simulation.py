import contextlib
import gc
import os
import runpy
import sys
from contextlib import asynccontextmanager
from copy import copy
from pathlib import Path
from typing import Callable, Optional, Union

import httpx
from starlette.routing import Route

from .. import app, binding, core, event, run, ui
from ..client import Client
from ..functions.download import download
from ..functions.navigate import Navigate
from ..functions.notify import notify
from .user import User


def prepare_simulation() -> None:
    """Prepare the simulation by adding the run config and setting the storage secret."""
    core.app.config.add_run_config(
        reload=False,
        title='Test App',
        viewport='',
        favicon=None,
        dark=False,
        language='en-US',
        binding_refresh_interval=0.1,
        reconnect_timeout=3.0,
        message_history_length=1000,
        tailwind=True,
        prod_js=True,
        show_welcome_message=False,
    )


@contextlib.contextmanager
def nicegui_reset_globals():
    """Reset the global state of the NiceGUI package."""
    for route in list(app.routes):
        if isinstance(route, Route) and (
            not route.path.startswith('/_nicegui/') or
            route.path.startswith('/_nicegui/auto/static') or
            route.path.startswith('/_nicegui/client/')
        ):
            app.remove_route(route.path)

    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    core.reset()

    element_types: list[type[ui.element]] = [ui.element, *find_all_subclasses(ui.element)]
    default_classes = {t: copy(t._default_classes) for t in element_types}  # pylint: disable=protected-access
    default_styles = {t: copy(t._default_style) for t in element_types}  # pylint: disable=protected-access
    default_props = {t: copy(t._default_props) for t in element_types}  # pylint: disable=protected-access

    Client.instances.clear()
    Client.page_routes.clear()
    app.reset()
    binding.reset()

    gc.collect()

    try:
        yield
    finally:
        gc.collect()

        app.reset()
        event.reset()
        run.reset()

        for t in element_types:
            t._default_classes = default_classes[t]  # pylint: disable=protected-access
            t._default_style = default_styles[t]  # pylint: disable=protected-access
            t._default_props = default_props[t]  # pylint: disable=protected-access

        for func in Client.page_routes:
            if not func.__module__.startswith('tests.'):
                sys.modules.pop(func.__module__, None)


def find_all_subclasses(cls: type) -> list[type]:
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(find_all_subclasses(subclass))
    return subclasses


@asynccontextmanager
async def user_simulation(
    root: Optional[Callable] = None, *, main_path: Optional[Union[str, bytes, os.PathLike]] = None
):
    """Context manager for test user simulation.

    Context manager that yields a ``User`` connected to a NiceGUI app within an isolated test context.

    :param root: root function for NiceGUI in script mode. It is passed directly to ``ui.run``; mutually exclusive with ``main_path`` argument.
    :param main_path: path to a NiceGUI main file executed via ``runpy.run_path``; mutually exclusive with ``root`` argument.
    """

    if main_path is not None and root is not None:
        raise ValueError('Cannot specify both `main_path` and `root` function simultaneously.')

    if root is not None and not callable(root):
        raise ValueError('`root` must be a callable or None')

    if main_path is not None:
        try:
            main_path = Path(main_path)
        except TypeError as e:
            raise TypeError('main_path must be convertible to Path') from e
        if not main_path.exists():
            raise FileNotFoundError(f'Main file not found at {main_path}')

    with nicegui_reset_globals():
        os.environ['NICEGUI_USER_SIMULATION'] = 'true'
        try:
            if main_path is not None:
                runpy.run_path(str(main_path), run_name='__main__')
            else:
                prepare_simulation()
                if root is None:
                    ui.run(storage_secret='simulated secret')
                else:
                    ui.run(root, storage_secret='simulated secret')

            async with core.app.router.lifespan_context(core.app):
                async with httpx.AsyncClient(transport=httpx.ASGITransport(core.app), base_url='http://test') as client:
                    user = User(client)
                    yield user
        finally:
            os.environ.pop('NICEGUI_USER_SIMULATION', None)
            ui.navigate = Navigate()
            ui.notify = notify
            ui.download = download
