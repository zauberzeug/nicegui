import os
import runpy
from collections.abc import AsyncGenerator
from typing import Callable

import httpx
import pytest

from nicegui import core, ui
from nicegui.functions.download import download
from nicegui.functions.navigate import Navigate
from nicegui.functions.notify import notify

from .general_fixtures import (  # noqa: F401  # pylint: disable=unused-import
    get_path_to_main_file,
    nicegui_reset_globals,
    prepare_simulation,
    pytest_addoption,
    pytest_configure,
)
from .user import User

# pylint: disable=redefined-outer-name


@pytest.fixture
async def user(nicegui_reset_globals,  # noqa: F811, pylint: disable=unused-argument
               caplog: pytest.LogCaptureFixture,
               request: pytest.FixtureRequest,
               ) -> AsyncGenerator[User, None]:
    """Create a new user fixture."""
    os.environ['NICEGUI_USER_SIMULATION'] = 'true'
    try:
        main_path = get_path_to_main_file(request)
        if main_path is None:
            prepare_simulation()
            ui.run(storage_secret='simulated secret')
        else:
            runpy.run_path(str(main_path), run_name='__main__')

        async with core.app.router.lifespan_context(core.app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(core.app), base_url='http://test') as client:
                yield User(client)

        logs = [record for record in caplog.get_records('call') if record.levelname == 'ERROR']
        if logs:
            pytest.fail('There were unexpected ERROR logs.', pytrace=False)
    finally:
        os.environ.pop('NICEGUI_USER_SIMULATION', None)
        ui.navigate = Navigate()
        ui.notify = notify
        ui.download = download


@pytest.fixture
async def create_user(user: User) -> AsyncGenerator[Callable[[], User], None]:  # pylint: disable=unused-argument
    """Create a fixture for building new users."""
    prepare_simulation()
    try:
        async with core.app.router.lifespan_context(core.app):
            yield lambda: User(httpx.AsyncClient(transport=httpx.ASGITransport(core.app), base_url='http://test'))
    finally:
        ui.navigate = Navigate()
        ui.notify = notify
        ui.download = download
