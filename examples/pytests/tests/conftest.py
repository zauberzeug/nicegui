from typing import Generator

import pytest
from pytests.startup import startup

from nicegui.testing import Screen, User

pytest_plugins = ['nicegui.testing.fixtures']


@pytest.fixture
def user(user: User) -> Generator[User, None, None]:
    startup()
    yield user


@pytest.fixture
def screen(screen: Screen) -> Generator[Screen, None, None]:
    startup()
    yield screen
