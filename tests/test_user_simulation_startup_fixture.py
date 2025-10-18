from typing import Callable

import pytest

from nicegui import app, ui
from nicegui.testing import User


@pytest.fixture
def user_startup_func() -> Callable[[], None]:
    def custom_startup():
        @ui.page('/')
        def page():
            ui.label('Hello from my custom startup :-)')

        ui.run()

    return custom_startup


# NOTE: this test is in a separate file to ensure the user_startup fixture override is only applied to this test
async def test_user_startup_fixture(user: User):
    await user.open('/')

    await user.should_see('Hello from my custom startup :-)')
    assert app.storage.secret is None, 'normally the startup sets a storage secret, but our custom startup does not'
