import os
import runpy
from collections.abc import AsyncGenerator
from typing import Callable

import httpx
import pytest

import nicegui
from nicegui import core, ui
from nicegui.functions.download import download
from nicegui.functions.navigate import Navigate
from nicegui.functions.notify import notify

from .general_fixtures import (  # noqa: F401  # pylint: disable=unused-import
    nicegui_reset_globals,
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
    runpy.run_path(request.config.getini('main_file'))
    async with core.app.router.lifespan_context(core.app):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(core.app), base_url='http://test') as client:
            yield User(client)
    ui.navigate = Navigate()
    ui.notify = notify
    ui.download = download

    logs = [record for record in caplog.get_records('call') if record.levelname == 'ERROR']
    if logs:
        pytest.fail('There were unexpected ERROR logs.', pytrace=False)


@pytest.fixture
async def create_user(nicegui_reset_globals,  # noqa: F811, pylint: disable=unused-argument
                      request: pytest.FixtureRequest,
                      ) -> AsyncGenerator[Callable[[], User], None]:
    """Create a fixture for building new users."""
    prepare_simulation()
    async with core.app.router.lifespan_context(core.app):
        yield lambda: User(httpx.AsyncClient(transport=httpx.ASGITransport(core.app), base_url='http://test'))
    ui.navigate = Navigate()
    ui.notify = notify
    ui.download = download


def prepare_simulation() -> None:
    """Prepare a simulation to be started.
    """
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
    nicegui.storage.set_storage_secret('simulated secret')
