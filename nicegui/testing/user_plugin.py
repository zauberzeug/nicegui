from collections.abc import AsyncGenerator, Callable

import httpx2
import pytest

from nicegui import core

from .general_fixtures import (  # noqa: F401  # pylint: disable=unused-import
    get_path_to_main_file,
    pytest_addoption,
    pytest_configure,
)
from .user import User
from .user_simulation import prepare_simulation, user_simulation

# pylint: disable=redefined-outer-name


@pytest.fixture
async def user(caplog: pytest.LogCaptureFixture, request: pytest.FixtureRequest) -> AsyncGenerator[User, None]:
    """Create a new user fixture."""
    async with user_simulation(main_file=get_path_to_main_file(request)) as user:
        yield user

        logs = [record for record in caplog.get_records('call') if record.levelname == 'ERROR']
        if logs:
            pytest.fail('There were unexpected ERROR logs.', pytrace=False)


@pytest.fixture
async def create_user(user: User) -> AsyncGenerator[Callable[[], User], None]:  # pylint: disable=unused-argument
    """Create a fixture for building new users."""
    prepare_simulation()
    async with core.app.router.lifespan_context(core.app):
        yield lambda: User(httpx2.AsyncClient(transport=httpx2.ASGITransport(core.app), base_url='http://test'))
