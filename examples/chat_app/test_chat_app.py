from typing import Callable

from nicegui import ui
from nicegui.testing import User


async def test_basic_startup_appearance(user: User) -> None:
    """Test basic appearance of the chat app."""
    await user.open('/')
    await user.should_see('simple chat app')
    await user.should_see('https://robohash.org/')
    await user.should_see('message')
    await user.should_see('No messages yet')


async def test_sending_messages(create_user: Callable[[], User]) -> None:
    """Test sending messages from two different screens."""
    user1 = create_user()
    user2 = create_user()

    await user1.open('/')
    user1.find(ui.input).type('Hello from screen A!').trigger('keydown.enter')
    await user1.should_see('Hello from screen A!')
    await user1.should_see('message')

    await user2.open('/')
    await user2.should_see('Hello from screen A!')
    user2.find(ui.input).type('Hello from screen B!').trigger('keydown.enter')
    await user2.should_see('message')

    await user1.should_see('Hello from screen A!')
    await user1.should_see('Hello from screen B!')
