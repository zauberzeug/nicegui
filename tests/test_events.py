import asyncio

from nicegui import ui

from .screen import Screen


def test_event_with_update_after_await(screen: Screen):
    @ui.page('/')
    def page():
        async def update():
            ui.label('1')
            await asyncio.sleep(1.0)
            ui.label('2')

        ui.button('update', on_click=update)

    screen.open('/')
    screen.click('update')
    screen.wait_for('1')
    screen.should_not_contain('2')
    screen.wait_for('2')
