import asyncio

import pytest

from nicegui import ui
from nicegui.testing import User

from . import main


@pytest.mark.module_under_test(main)
async def test_basic_startup_appearance(user: User) -> None:
    """Test basic appearance of the chat app."""
    await user.open('/')
    await user.should_see(content='simple chat app')
    await user.should_see(content='https://robohash.org/')
    await user.should_see(content='message')
    await user.should_see(content='No messages yet')


@pytest.mark.module_under_test(main)
async def test_sending_messages(user_builder) -> None:
    """Test sending messages from two different screens."""

    userA = user_builder()
    userB = user_builder()
    await userA.open('/')
    userA.type(text='Hello from screen A!', element=ui.input)
    await userA.should_see(content='Hello from screen A!')
    await userA.should_see(content='message')
    await userB.open('/')
    await userB.should_see(content='Hello from screen A!')
    userB.type(text='Hello, from screen B!', element=ui.input)
    await userB.should_see(content='message')

    userA.activate()
    await userA.should_see(content='Hello from screen A!')
    await userA.should_see(content='Hello, from screen B!')
