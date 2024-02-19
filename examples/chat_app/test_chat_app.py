import asyncio

import pytest

from nicegui import ui
from nicegui.testing import SimulatedScreen

from . import main


@pytest.mark.module_under_test(main)
async def test_basic_startup_appearance(screen: SimulatedScreen) -> None:
    """Test basic appearance of the chat app."""
    with await screen.open('/') as user:
        user.should_see(content='simple chat app')
        user.should_see(content='https://robohash.org/')
        user.should_see(content='message')
        await user.should_see(content='No messages yet')


@pytest.mark.module_under_test(main)
async def test_sending_messages(screen: SimulatedScreen) -> None:
    """Test sending messages from two different screens."""
    with await screen.open('/') as userA:
        userA.type(text='Hello from screen A!', element=ui.input)
        userA.should_see(content='Hello from screen A!')
        userA.should_see(content='message')
    with await screen.open('/')as userB:
        userB.should_see(content='Hello from screen A!')
        userB.type(text='Hello, from screen B!', element=ui.input)
        userB.should_see(content='message')
    with userA:
        userA.should_see(content='Hello from screen A!')
        userA.should_see(content='Hello, from screen B!')
