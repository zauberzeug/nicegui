from typing import Callable

import pytest

from nicegui import ui
from nicegui.testing import User

from . import main


@pytest.mark.module_under_test(main)
async def test_basic_startup_appearance(user: User) -> None:
    """Test basic appearance of the chat app."""
    await user.open('/')
    await user.should_see('simple chat app')
    await user.should_see('https://robohash.org/')
    await user.should_see('message')
    await user.should_see('No messages yet')


@pytest.mark.module_under_test(main)
async def test_sending_messages(create_user: Callable[[], User]) -> None:
    """Test sending messages from two different screens."""
    userA = create_user()
    userB = create_user()

    await userA.open('/')
    userA.find(ui.input).type('Hello from screen A!').trigger('keydown.enter')
    await userA.should_see('Hello from screen A!')
    await userA.should_see('message')

    await userB.open('/')
    await userB.should_see('Hello from screen A!')
    userB.find(ui.input).type('Hello from screen B!').trigger('keydown.enter')
    await userB.should_see('message')

    await userA.should_see('Hello from screen A!')
    await userA.should_see('Hello from screen B!')
