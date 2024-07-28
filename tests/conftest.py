# pylint: disable=wildcard-import,unused-wildcard-import
from typing import AsyncGenerator, Generator

import pytest

from nicegui.testing import Screen, User


@pytest.fixture
def screen(nicegui_screen: Screen) -> Generator[Screen, None, None]:
    yield nicegui_screen


@pytest.fixture
async def user(nicegui_user: User) -> AsyncGenerator[User, None]:
    yield nicegui_user
