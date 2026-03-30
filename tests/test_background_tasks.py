import asyncio
import gc
from collections.abc import Callable

import pytest

from nicegui import app, background_tasks, ui
from nicegui.testing import Screen, User

# pylint: disable=missing-function-docstring


# NOTE: click handlers, and system events used to wrap background_task in a background_task (see https://github.com/zauberzeug/nicegui/pull/4641#issuecomment-2837448265)
@pytest.mark.parametrize('strategy', ['direct', 'click', 'system'])
async def test_awaiting_background_tasks_on_shutdown(user: User, strategy: str):
    run = set()
    cancelled = set()

    async def one():
        try:
            run.add('one')
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            cancelled.add('one')

    @background_tasks.await_on_shutdown
    async def two():
        try:
            run.add('two')
            await asyncio.sleep(1)
            background_tasks.create(three(), name='three')
            background_tasks.create(four(), name='four')
        except asyncio.CancelledError:
            cancelled.add('two')

    async def three():
        try:
            await asyncio.sleep(0.1)
            run.add('three')
        except asyncio.CancelledError:
            cancelled.add('three')

    @background_tasks.await_on_shutdown
    async def four():
        try:
            await asyncio.sleep(0.1)
            run.add('four')
        except asyncio.CancelledError:
            cancelled.add('four')

    @ui.page('/')
    def page():
        ui.button('One', on_click=lambda: background_tasks.create(one(), name='one'))
        ui.button('Two', on_click=lambda: background_tasks.create(two(), name='two'))

    if strategy == 'system':
        app.on_connect(lambda: background_tasks.create(one(), name='one'))
        app.on_connect(lambda: background_tasks.create(two(), name='two'))

    await user.open('/')

    if strategy == 'click':
        user.find('One').click()
        user.find('Two').click()
    elif strategy == 'direct':
        background_tasks.create(one(), name='one')
        background_tasks.create(two(), name='two')

    await asyncio.sleep(0.1)  # NOTE: we need to wait for the tasks to be created

    # NOTE: teardown is called on shutdown; here we call it directly to test the teardown logic while test is still running
    await background_tasks.teardown()
    assert cancelled == {'one', 'three'}
    assert run == {'one', 'two', 'four'}


@pytest.mark.parametrize('create', [background_tasks.create, background_tasks.create_lazy])
async def test_inner_async_function_is_awaited_on_shutdown(user: User, create: Callable):
    events: list[str] = []

    @ui.page('/')
    def page():
        @background_tasks.await_on_shutdown
        async def inner():
            try:
                await asyncio.sleep(0.05)
                events.append('inner ran')
            except asyncio.CancelledError:
                events.append('inner cancelled')
        create(inner(), name='inner')

    await user.open('/')

    for _ in range(3):
        await asyncio.sleep(0)
        gc.collect()

    await background_tasks.teardown()
    assert events == ['inner ran']


def test_create_tasks(screen: Screen) -> None:
    events: list[str] = []

    async def async_function(name: str) -> None:
        events.append(name)
        await asyncio.sleep(1.0)

    # create before loop started
    with pytest.raises(AssertionError):
        background_tasks.create(a := async_function('A'))
    a.close()
    with pytest.raises(AssertionError):
        background_tasks.create_lazy(b := async_function('B'), name='B')
    b.close()

    # create or defer before loop started
    background_tasks.create_or_defer(async_function('C1'))
    background_tasks.create_or_defer(async_function('C2'))
    background_tasks.create_lazy_or_defer(async_function('D1'), name='D')
    background_tasks.create_lazy_or_defer(async_function('D2'), name='D')  # dropped because D1 is still busy

    @ui.page('/')
    def page():
        # create after loop started
        background_tasks.create(async_function('E1'))
        background_tasks.create(async_function('E2'))
        background_tasks.create_lazy(async_function('F1'), name='F')
        background_tasks.create_lazy(async_function('F2'), name='F')  # dropped because F1 is still busy

        # create or defer after loop started
        background_tasks.create_or_defer(async_function('G1'))
        background_tasks.create_or_defer(async_function('G2'))
        background_tasks.create_lazy_or_defer(async_function('H1'), name='H')
        background_tasks.create_lazy_or_defer(async_function('H2'), name='H')  # dropped because H1 is still busy

    screen.open('/')
    assert events == [
        'C1', 'C2',
        'D1',
        'E1', 'E2',
        'F1',
        'G1', 'G2',
        'H1',
    ]
