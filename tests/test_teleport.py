from nicegui import ui
from nicegui.testing import Screen


def test_should_work(screen: Screen):
    ui.row().classes('src')

    def create_teleport():
        with ui.teleport('.src'):
            ui.label('Hello')

    ui.button('create',on_click=create_teleport)

    screen.open('/')
    screen.click('create')
    assert screen.find_by_css('.src > div').text == 'Hello'


def test_update(screen: Screen):
    pass

