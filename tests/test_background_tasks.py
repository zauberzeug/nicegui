import asyncio

import pytest

from nicegui import background_tasks, ui
from nicegui.testing import User

# pylint: disable=missing-function-docstring


# NOTE: click handlers used to wrap background_task in a background_task (see https://github.com/zauberzeug/nicegui/pull/4641#issuecomment-2837448265)
@pytest.mark.parametrize('with_click_handler', [False, True])
async def test_awaiting_background_tasks_on_shutdown(user: User, with_click_handler: bool):

    async def one():
        nonlocal cancelled_one
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            cancelled_one = True

    @background_tasks.await_on_shutdown
    async def two():
        nonlocal cancelled_two
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            cancelled_two = True

    cancelled_one = False
    cancelled_two = False
    ui.button('One', on_click=lambda: background_tasks.create(one(), name='one'))
    ui.button('Two', on_click=lambda: background_tasks.create(two(), name='two'))

    await user.open('/')
    if with_click_handler:
        user.find('One').click()
        user.find('Two').click()
    else:
        background_tasks.create(one(), name='one')
        background_tasks.create(two(), name='two')

    await asyncio.sleep(0.1)  # NOTE: we need to wait for the tasks to be created

    # NOTE: teardown is called on shutdown; here we call it directly to test the teardown logic while test is still running
    await background_tasks.teardown()
    assert cancelled_one
    assert not cancelled_two
