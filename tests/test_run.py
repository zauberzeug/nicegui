import asyncio
import time
from typing import Awaitable, Generator, Optional

import pytest

from nicegui import app, run, ui
from nicegui.testing import User


@pytest.fixture(scope='module', autouse=True)
def check_blocking_ui() -> Generator[None, None, None]:
    """This fixture ensures that we see a warning if the UI is blocked for too long.
    The warning would then automatically fail the test."""
    loop: Optional[asyncio.AbstractEventLoop] = None

    def configure() -> None:
        loop = asyncio.get_running_loop()
        loop.set_debug(True)
        loop.slow_callback_duration = 0.02
    app.on_startup(configure)
    yield
    if loop:
        loop.set_debug(False)


def delayed_hello() -> str:
    """Test function that blocks for 1 second."""
    time.sleep(1)
    return 'hello'


@pytest.mark.parametrize('func', [run.cpu_bound, run.io_bound])
async def test_delayed_hello(user: User, func: Awaitable):

    @ui.page('/')
    async def index():
        ui.label(await func(delayed_hello))

    await user.open('/')
    await user.should_see('hello')
