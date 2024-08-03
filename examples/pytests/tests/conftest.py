from typing import Generator

import pytest
from app.startup import startup

from nicegui.testing import Screen, User

pytest_plugins = ['nicegui.testing.plugin']


@pytest.fixture
def user(user: User) -> Generator[User, None, None]:
    startup()
    yield user


@pytest.fixture
def screen(screen: Screen) -> Generator[Screen, None, None]:
    startup()
    yield screen
