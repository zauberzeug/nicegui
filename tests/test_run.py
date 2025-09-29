import asyncio
import os
import time
from collections.abc import Awaitable, Generator
from concurrent.futures.process import BrokenProcessPool

import pytest

from nicegui import app, run, ui
from nicegui.testing import User


@pytest.fixture(scope='module', autouse=True)
def check_blocking_ui() -> Generator[None, None, None]:
    """This fixture ensures that we see a warning if the UI is blocked for too long.

    The warning would then automatically fail the test.
    """
    def configure() -> None:
        loop = asyncio.get_running_loop()
        loop.set_debug(True)
        loop.slow_callback_duration = 0.02
    app.on_startup(configure)
    yield


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


async def test_run_unpickable_exception_in_cpu_bound_callback(user: User):
    class UnpicklableException(Exception):
        def __reduce__(self):
            raise NotImplementedError('This local object cannot be pickled')

    def raise_unpicklable_exception():
        raise UnpicklableException('test')

    @ui.page('/')
    async def index():
        with pytest.raises(AttributeError, match="Can't pickle local object|Can't get local object"):
            ui.label(await run.cpu_bound(raise_unpicklable_exception))

    await user.open('/')


class ExceptionWithSuperParameter(Exception):
    def __init__(self) -> None:
        super().__init__('some parameter which does not appear in the custom exceptions init')


def raise_exception_with_super_parameter():
    raise ExceptionWithSuperParameter()


async def test_run_cpu_bound_function_which_raises_problematic_exception(user: User):
    @ui.page('/')
    async def index():
        with pytest.raises(run.SubprocessException, match='some parameter which does not appear in the custom exceptions init'):
            ui.label(await run.cpu_bound(raise_exception_with_super_parameter))

    await user.open('/')


async def test_run_cpu_bound_survive_bad_function(user: User):
    @ui.page('/')
    async def index():
        with pytest.raises(BrokenProcessPool):
            await run.cpu_bound(os.abort)  # bad function kills the process pool
        assert isinstance(await run.cpu_bound(time.time), float)  # good function returns without error
        ui.label('excellent')

    await user.open('/')
    await user.should_see('excellent')
