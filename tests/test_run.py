import asyncio
import multiprocessing
import os
import time
from collections.abc import Callable, Generator
from concurrent.futures.process import BrokenProcessPool
from pickle import PicklingError

import pytest

from nicegui import app, run, ui
from nicegui.app.app import State
from nicegui.helpers import warnings as nicegui_warnings
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
async def test_delayed_hello(user: User, func: Callable):
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
        with pytest.raises((AttributeError, PicklingError), match=r"Can't pickle local object|Can't get local object"):
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


def bad_function() -> None:
    os._exit(1)  # pylint: disable=protected-access


def good_function() -> bool:
    return True


async def test_run_cpu_bound_survive_bad_function(user: User):
    @ui.page('/')
    async def index():
        with pytest.raises(BrokenProcessPool):
            await run.cpu_bound(bad_function)
        assert await run.cpu_bound(good_function)
        ui.label('excellent')

    await user.open('/')
    await user.should_see('excellent')


@pytest.mark.parametrize('func', [run.cpu_bound, run.io_bound])
async def test_returns_none_when_app_is_stopping(user: User, func: Callable):
    @ui.page('/')
    async def index():
        original_state = app._state  # pylint: disable=protected-access
        app._state = State.STOPPING  # pylint: disable=protected-access
        try:
            result = await func(delayed_hello)
            ui.label(f'result={result}')
        finally:
            app._state = original_state  # pylint: disable=protected-access

    await user.open('/')
    await user.should_see('result=None')


@pytest.fixture
def isolate_pool_state() -> Generator[None, None, None]:
    """Restore run.process_pool_start_method, drop the test's pool and forget shown warnings."""
    original = run.process_pool_start_method
    nicegui_warnings.reset()
    try:
        yield
    finally:
        run.process_pool_start_method = original
        run.reset()
        nicegui_warnings.reset()


@pytest.mark.parametrize('method', [None, 'spawn', 'fork', 'forkserver'])
def test_pool_uses_configured_start_method(isolate_pool_state, method):
    """setup() builds the pool with the configured start method (or the platform default for None)."""
    if method is not None and method not in multiprocessing.get_all_start_methods():
        pytest.skip(f'{method} is not available on this platform')
    run.process_pool_start_method = method
    run.setup()
    expected = multiprocessing.get_start_method() if method is None else method
    assert run.process_pool is not None
    assert run.process_pool._mp_context is not None  # pylint: disable=protected-access
    assert run.process_pool._mp_context.get_start_method() == expected  # pylint: disable=protected-access


def test_spawn_pool_reuses_shared_spawn_context(isolate_pool_state):
    """A "spawn" pool reuses the module-level SPAWN_CONTEXT shared with native.py (no duplicate context)."""
    run.process_pool_start_method = 'spawn'
    run.setup()
    assert run.process_pool is not None
    assert run.process_pool._mp_context is run.SPAWN_CONTEXT  # pylint: disable=protected-access


def test_invalid_start_method_fails_at_setup(isolate_pool_state):
    """An unknown value (or one the platform lacks, e.g. "fork" on Windows) makes setup() fail fast."""
    run.process_pool_start_method = 'bogus'  # type: ignore[assignment]
    with pytest.raises(ValueError, match=r'Invalid run\.process_pool_start_method'):
        run.setup()


@pytest.mark.parametrize('method,expect_warning', [(None, True), ('spawn', False), ('fork', False)])
async def test_fork_heads_up_warning(isolate_pool_state, caplog, method, expect_warning):
    """The one-time heads-up fires iff the start method was never chosen and the pool falls back to fork."""
    if method != 'spawn' and multiprocessing.get_start_method() != 'fork':
        pytest.skip('needs a platform with a fork default (e.g. Linux)')
    run.process_pool_start_method = method
    run.setup()
    assert await run.cpu_bound(good_function)
    assert ('process_pool_start_method' in caplog.text) is expect_warning


async def test_warning_reflects_pool_not_later_setting_change(isolate_pool_state, caplog):
    """Flipping the setting after startup must not silence the heads-up about the still-fork live pool."""
    if multiprocessing.get_start_method() != 'fork':
        pytest.skip('needs a platform with a fork default (e.g. Linux)')
    run.process_pool_start_method = None
    run.setup()
    run.process_pool_start_method = 'spawn'  # too late, the pool is already built
    assert await run.cpu_bound(good_function)
    assert 'process_pool_start_method' in caplog.text
