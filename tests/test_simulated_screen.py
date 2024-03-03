import asyncio

import pytest

from nicegui import ElementFilter, ui
from nicegui.testing import SimulatedScreen

# pylint: disable=missing-function-docstring


async def test_multiple_pages(screen: SimulatedScreen) -> None:
    @ui.page('/')
    def index():
        ui.label('Main page')

    @ui.page('/other')
    def other():
        ui.label('Other page')

    with await screen.open('/') as userA:
        await userA.should_see(content='Main page')
    with await screen.open('/other') as userB:
        await userB.should_see(content='Other page')
    with userA:
        await userA.should_see(content='Main page')
    with userB:
        await userB.should_see(content='Other page')


async def test_source_element(screen: SimulatedScreen) -> None:
    @ui.page('/')
    def index():
        ui.image('https://via.placeholder.com/150')

    with await screen.open('/') as user:
        await user.should_see(content='placeholder.com')


async def test_assertion_raised_when_element_not_found(screen: SimulatedScreen) -> None:
    @ui.page('/')
    def index():
        ui.label('Hello')

    with await screen.open('/') as user:
        with pytest.raises(AssertionError):
            await user.should_see(content='World')
