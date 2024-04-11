import asyncio
import time
from typing import Awaitable, Generator, Optional

import pytest

from nicegui import app, run, ui
from nicegui.testing import Screen


@pytest.fixture(scope='module', autouse=True)
def check_blocking_ui() -> Generator[None, None, None]:
    loop: Optional[asyncio.AbstractEventLoop] = None

    def configure() -> None:
        loop = asyncio.get_running_loop()
        loop.set_debug(True)
        loop.slow_callback_duration = 0.02
    app.on_startup(configure)
    app.on_shutdown(lambda: loop and loop.set_debug(False))
    yield


def delayed_hello() -> str:
    """Test function that blocks for 1 second."""
    time.sleep(1)
    return 'hello'


@pytest.mark.parametrize('func', [run.cpu_bound, run.io_bound])
def test_delayed_hello(screen: Screen, func: Awaitable):

    @ui.page('/')
    async def index():
        ui.label(await func(delayed_hello))

    screen.open('/')
    screen.should_contain('hello')
