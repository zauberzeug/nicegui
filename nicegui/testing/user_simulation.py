import os
import runpy
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Callable, Optional, Union

import httpx

from .. import core, ui
from ..functions.download import download
from ..functions.navigate import Navigate
from ..functions.notify import notify
from .general import nicegui_reset_globals, prepare_simulation
from .user import User


@asynccontextmanager
async def user_simulation(
    root: Optional[Callable] = None, *, main_file: Optional[Union[str, os.PathLike]] = None
) -> AsyncGenerator[User, None]:
    """Context manager for test user simulation.

    Context manager that yields a ``User`` connected to a NiceGUI app within an isolated test context.

    :param root: root function which is passed directly to ``ui.run``; mutually exclusive with ``main_file`` argument.
    :param main_file: path to a NiceGUI main file executed via ``runpy.run_path``; mutually exclusive with ``root`` argument.
    """

    if main_file is not None and root is not None:
        raise ValueError('Cannot specify both `main_file` and `root` function simultaneously.')

    if root is not None and not callable(root):
        raise ValueError('`root` must be a callable or None')

    if main_file is not None:
        try:
            main_file_path = Path(main_file)
        except TypeError as e:
            raise TypeError('main_file must be convertible to Path') from e
        if not main_file_path.exists():
            raise FileNotFoundError(f'Main file not found at {main_file_path}')

    with nicegui_reset_globals():
        os.environ['NICEGUI_USER_SIMULATION'] = 'true'
        try:
            if main_file is not None:
                runpy.run_path(str(main_file_path), run_name='__main__')
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
