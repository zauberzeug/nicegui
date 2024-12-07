import asyncio
from typing import AsyncGenerator, Callable

import httpx
import pytest

from nicegui import Client, core, ui
from nicegui.functions.navigate import Navigate
from nicegui.functions.notify import notify

from .general_fixtures import (  # noqa: F401  # pylint: disable=unused-import
    nicegui_reset_globals,
    prepare_simulation,
    pytest_configure,
)
from .user import User

# pylint: disable=redefined-outer-name


@pytest.fixture()
def prepare_simulated_auto_index_client(request):
    """Prepare the simulated auto index client."""
    original_test = request.node._obj  # pylint: disable=protected-access
    if asyncio.iscoroutinefunction(original_test):
        async def wrapped_test(*args, **kwargs):
            with Client.auto_index_client:
                return await original_test(*args, **kwargs)
        request.node._obj = wrapped_test  # pylint: disable=protected-access
    else:
        def wrapped_test(*args, **kwargs):
            Client.auto_index_client.__enter__()  # pylint: disable=unnecessary-dunder-call
            return original_test(*args, **kwargs)
        request.node._obj = wrapped_test  # pylint: disable=protected-access


@pytest.fixture
async def user(nicegui_reset_globals,  # noqa: F811, pylint: disable=unused-argument
               prepare_simulated_auto_index_client,  # pylint: disable=unused-argument
               request: pytest.FixtureRequest,
               ) -> AsyncGenerator[User, None]:
    """Create a new user fixture."""
    prepare_simulation(request)
    async with core.app.router.lifespan_context(core.app):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(core.app), base_url='http://test') as client:
            yield User(client)
    ui.navigate = Navigate()
    ui.notify = notify


@pytest.fixture
async def create_user(nicegui_reset_globals,  # noqa: F811, pylint: disable=unused-argument
                      prepare_simulated_auto_index_client,  # pylint: disable=unused-argument
                      request: pytest.FixtureRequest,
                      ) -> AsyncGenerator[Callable[[], User], None]:
    """Create a fixture for building new users."""
    prepare_simulation(request)
    async with core.app.router.lifespan_context(core.app):
        yield lambda: User(httpx.AsyncClient(transport=httpx.ASGITransport(core.app), base_url='http://test'))
    ui.navigate = Navigate()
    ui.notify = notify
