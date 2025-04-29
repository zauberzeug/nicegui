import asyncio

from nicegui import background_tasks, ui
from nicegui.testing import User

# pylint: disable=missing-function-docstring


async def test_awaiting_background_tasks_on_shutdown(user: User):

    async def one():
        nonlocal cancelled_one
        try:
            print('one start')
            await asyncio.sleep(1)
            print('one end')
        except asyncio.CancelledError:
            cancelled_one = True

    @background_tasks.await_on_shutdown
    async def two():
        nonlocal cancelled_two
        try:
            print('two start')
            await asyncio.sleep(1)
            print('two end')
        except asyncio.CancelledError:
            cancelled_two = True

    cancelled_one = False
    cancelled_two = False

    await user.open('/')
    background_tasks.create(one(), name='one')
    background_tasks.create(two(), name='two')
    await asyncio.sleep(0.1)
    # NOTE: teardown is called on shutdown; here we call it directly to test the teardown logic while test is still running
    await background_tasks.teardown()
    assert cancelled_one
    assert not cancelled_two


async def test_awaiting_click_handler_background_tasks_on_shutdown(user: User):

    async def one():
        nonlocal cancelled_one
        try:
            print('one start')
            await asyncio.sleep(1)
            print('one end')
        except asyncio.CancelledError:
            cancelled_one = True

    @background_tasks.await_on_shutdown
    async def two():
        nonlocal cancelled_two
        try:
            print('two start')
            await asyncio.sleep(1)
            print('two end')
        except asyncio.CancelledError:
            cancelled_two = True

    cancelled_one = False
    cancelled_two = False
    ui.button('One', on_click=lambda: background_tasks.create(one(), name='one'))
    ui.button('Two', on_click=lambda: background_tasks.create(two(), name='two'))

    await user.open('/')
    user.find('One').click()
    user.find('Two').click()
    # NOTE: teardown is called on shutdown; here we call it directly to test the teardown logic while test is still running
    await background_tasks.teardown()
    assert cancelled_one
    assert not cancelled_two
