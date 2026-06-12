import os
import runpy
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from pathlib import Path

import httpx

from .. import core, ui
from ..functions.download import download
from ..functions.navigate import Navigate
from ..functions.notify import notify
from .general import nicegui_reset_globals, prepare_simulation
from .user import User


@asynccontextmanager
async def user_simulation(
    root: Callable | None = None, *, main_file: str | os.PathLike | None = None,
) -> AsyncGenerator[User]:
    """Context manager for test user simulation.

    This context manager yields a ``User`` connected to a NiceGUI app within an isolated test context.

    :param root: root function which is passed directly to ``ui.run``; mutually exclusive with ``main_file`` argument.
    :param main_file: path to a NiceGUI main file executed via ``runpy.run_path``; mutually exclusive with ``root`` argument.
    """
    if main_file is not None and root is not None:
        raise ValueError('Cannot specify both `main_file` and `root` function simultaneously.')

    with nicegui_reset_globals():
        os.environ['NICEGUI_USER_SIMULATION'] = 'true'
        try:
            if main_file is not None:
                if not Path(main_file).exists():
                    raise FileNotFoundError(f'Main file not found at {main_file}')
                runpy.run_path(str(main_file), run_name='__main__')
            else:
                prepare_simulation()
                ui.run(root, storage_secret='simulated secret')

            async with core.app.router.lifespan_context(core.app):
                async with httpx.AsyncClient(transport=httpx.ASGITransport(core.app), base_url='http://test') as client:
                    yield User(client)
        finally:
            os.environ.pop('NICEGUI_USER_SIMULATION', None)
            ui.navigate = Navigate()
            ui.notify = notify
            ui.download = download
