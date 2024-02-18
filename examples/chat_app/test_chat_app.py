import asyncio

import pytest

import main
from nicegui.testing import SimulatedScreen

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_start_screen(screen: SimulatedScreen) -> None:
    with await screen.open('/'):
        await screen.should_contain('simple chat app')
        await screen.should_contain('https://robohash.org/')
        await screen.should_contain('message')
        await asyncio.sleep(1)
        await screen.should_contain('no messages yet')


@pytest.mark.module_under_test(main)
async def test_sending_message(screen: SimulatedScreen) -> None:
    with await screen.open('/') as screenA:
        screen.type(target='message', content='Hello, chat!', confirmation='keydown.enter')
        await screen.should_contain('Hello, chat!')
    with await screen.open('/') as screenB:
        await screen.should_contain('Hello, chat!')
