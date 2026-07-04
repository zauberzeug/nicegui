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
def restore_start_method() -> Generator[None, None, None]:
    """Restore run.process_pool_start_method after a test that mutates it."""
    original = run.process_pool_start_method
    yield
    run.process_pool_start_method = original


@pytest.fixture
def isolate_pool_state() -> Generator[None, None, None]:
    """Save/restore the knob + latched pool state and clear shown warnings around the test."""
    original_method = run.process_pool_start_method
    original_context = run._pool_context  # pylint: disable=protected-access
    original_implicit_fork = run._pool_uses_implicit_fork  # pylint: disable=protected-access
    nicegui_warnings.reset()
    try:
        yield
    finally:
        run.reset()
        run.process_pool_start_method = original_method
        run._pool_context = original_context  # pylint: disable=protected-access
        run._pool_uses_implicit_fork = original_implicit_fork  # pylint: disable=protected-access
        nicegui_warnings.reset()


@pytest.mark.parametrize('method', [None, 'spawn', 'fork'])
def test_cpu_bound_context_resolution(restore_start_method, method):
    """The tri-state setting resolves to the expected multiprocessing start method."""
    if method == 'fork' and 'fork' not in multiprocessing.get_all_start_methods():
        pytest.skip('fork is not available on this platform')
    run.process_pool_start_method = method
    expected = multiprocessing.get_start_method() if method is None else method
    assert run._resolve_cpu_bound_context().get_start_method() == expected  # pylint: disable=protected-access


def test_cpu_bound_spawn_reuses_shared_spawn_context(restore_start_method):
    """'spawn' reuses the module-level SPAWN_CONTEXT shared with native.py (no duplicate context)."""
    run.process_pool_start_method = 'spawn'
    assert run._resolve_cpu_bound_context() is run.SPAWN_CONTEXT  # pylint: disable=protected-access


def test_cpu_bound_invalid_start_method_raises(restore_start_method):
    """An unsupported value fails fast with a clear message rather than deep inside pool setup."""
    run.process_pool_start_method = 'forkserver'  # a real mp method, but not a supported tri-state value
    with pytest.raises(ValueError, match=r'Invalid run\.process_pool_start_method'):
        run._resolve_cpu_bound_context()  # pylint: disable=protected-access


def test_cpu_bound_fork_unavailable_gives_clear_error(restore_start_method, monkeypatch):
    """An explicit 'fork' on a platform without it (e.g. Windows) gives a clear error, not a raw ValueError."""
    real_get_context = multiprocessing.get_context

    def fake_get_context(method=None):
        if method == 'fork':
            raise ValueError("cannot find context for 'fork'")  # what multiprocessing raises on Windows
        return real_get_context(method)

    monkeypatch.setattr(multiprocessing, 'get_context', fake_get_context)
    run.process_pool_start_method = 'fork'
    with pytest.raises(ValueError, match='not available on this platform'):
        run._resolve_cpu_bound_context()  # pylint: disable=protected-access


@pytest.mark.parametrize('method', [None, 'spawn', 'fork'])
def test_setup_latches_implicit_fork(isolate_pool_state, method):
    """setup() latches "implicit fork" iff the user never chose a method AND the pool resolves to fork."""
    if method == 'fork' and 'fork' not in multiprocessing.get_all_start_methods():
        pytest.skip('fork is not available on this platform')
    expected = method is None and multiprocessing.get_start_method() == 'fork'
    run.process_pool_start_method = method
    run.setup()
    assert run._pool_uses_implicit_fork is expected  # pylint: disable=protected-access


@pytest.mark.parametrize('implicit_fork,expect_warn', [(True, True), (False, False)])
def test_warn_fires_only_when_pool_uses_implicit_fork(isolate_pool_state, caplog, implicit_fork, expect_warn):
    """The heads-up is gated purely on the latched pool state, so it always describes the live pool."""
    run._pool_uses_implicit_fork = implicit_fork  # pylint: disable=protected-access
    run._warn_if_implicit_fork()  # pylint: disable=protected-access
    assert ('process_pool_start_method' in caplog.text) is expect_warn


def test_warn_reflects_pool_not_later_setting_change(isolate_pool_state):
    """Mutating the knob after setup() must not silence the heads-up about the still-fork live pool."""
    if multiprocessing.get_start_method() != 'fork':
        pytest.skip('needs a fork default to build an implicit-fork pool')
    run.process_pool_start_method = None
    run.setup()
    assert run._pool_uses_implicit_fork is True  # pylint: disable=protected-access
    run.process_pool_start_method = 'spawn'  # user flips the knob AFTER the pool is already built
    run._warn_if_implicit_fork()  # pylint: disable=protected-access
    # the latch (and therefore the heads-up) still describes the live pool, which is still fork:
    assert run._pool_uses_implicit_fork is True  # pylint: disable=protected-access
    assert any('process_pool_start_method' in m
               for m in nicegui_warnings._shown_warnings)  # pylint: disable=protected-access
