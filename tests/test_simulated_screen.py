import asyncio

from nicegui import ElementFilter, ui
from nicegui.testing import SimulatedScreen


async def test_multiple_pages(screen: SimulatedScreen) -> None:
    @ui.page('/')
    def index():
        ui.label('Main page')

    @ui.page('/other')
    def other():
        ui.label('Other page')

    with await screen.open('/') as userA:
        userA.should_see(content='Main page')
    with await screen.open('/other') as userB:
        userB.should_see(content='Other page')
    with userA:
        userA.should_see(content='Main page')
    with userB:
        userB.should_see(content='Other page')


async def test_source_element(screen: SimulatedScreen) -> None:
    @ui.page('/')
    def index():
        ui.image('https://via.placeholder.com/150')

    with await screen.open('/') as user:
        user.should_see(content='placeholder.com')
