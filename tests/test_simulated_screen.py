from nicegui import ui
from nicegui.testing import SimulatedScreen


async def test_multiple_pages(screen: SimulatedScreen) -> None:
    @ui.page('/')
    def index():
        ui.label('Main page')

    @ui.page('/other')
    def other():
        ui.label('Other page')

    with await screen.open('/') as main_screen:
        await screen.should_contain('Main page')
    with await screen.open('/other') as other_screen:
        await screen.should_contain('Other page')
    with main_screen:
        await screen.should_contain('Main page')
    with other_screen:
        await screen.should_contain('Other page')
