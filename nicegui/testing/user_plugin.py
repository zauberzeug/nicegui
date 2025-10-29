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
def user_startup_func(request: pytest.FixtureRequest) -> Callable[[], None]:
    """Return a startup function that initializes the NiceGUI app for testing.

    Executes configured main file, or prepares a basic setup if '' is provided.
    Can be replaced to provide fully customized startup behavior (see https://nicegui.io/documentation/user#using_pytest_fixtures_to_startup_your_app).
    """
    def startup():
        main_path = get_path_to_main_file(request)
        if main_path is None:
            prepare_simulation()
            ui.run(storage_secret='simulated secret')
        else:
            runpy.run_path(str(main_path), run_name='__main__')

    return startup


@pytest.fixture
async def user(nicegui_reset_globals,  # noqa: F811, pylint: disable=unused-argument
               caplog: pytest.LogCaptureFixture,
               user_startup_func: Callable[[], None],
               ) -> AsyncGenerator[User, None]:
    """Simulate a user interacting with the NiceGUI app without starting a real browser."""
    os.environ['NICEGUI_USER_SIMULATION'] = 'true'
    try:
        user_startup_func()

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
