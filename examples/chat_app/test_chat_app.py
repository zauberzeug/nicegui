import pytest

import main
from nicegui.testing import SimulatedScreen


@pytest.mark.module_under_test(main)
async def test_basic_startup_appearance(screen: SimulatedScreen) -> None:
    """Test the basic appearance of the chat app."""
    with await screen.open('/'):
        await screen.should_contain('simple chat app')
        await screen.should_contain('https://robohash.org/')
        await screen.should_contain('message')
        await screen.should_contain('No messages yet')


@pytest.mark.module_under_test(main)
async def test_sending_messages(screen: SimulatedScreen) -> None:
    """Test sending messages from two different screens."""
    with await screen.open('/') as screenA:
        screen.type(target='message', content='Hello from screen A!', confirmation='keydown.enter')
        await screen.should_contain('Hello from screen A!')
        await screen.should_contain('message')
    with await screen.open('/'):
        await screen.should_contain('Hello from screen A!')
        screen.type(target='message', content='Hello, from screen B!', confirmation='keydown.enter')
        await screen.should_contain('message')
    with screenA:
        await screen.should_contain('Hello from screen A!')
        await screen.should_contain('Hello, from screen B!')
