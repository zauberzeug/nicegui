from typing import Optional

from nicegui import ui
from nicegui.testing import Screen


def test_should_work(screen: Screen):
    ui.row().classes('src')

    def create_teleport():
        with ui.teleport('.src'):
            ui.label('Hello')

    ui.button('create', on_click=create_teleport)

    screen.open('/')
    screen.click('create')
    assert screen.find_by_css('.src > div').text == 'Hello'


def test_force_update(screen: Screen):
    tp: Optional[ui.teleport] = None

    box = ui.row().classes('src')

    def create_teleport():
        nonlocal tp
        with ui.teleport('.src') as tp:
            ui.label('Hello')

    ui.button('create', on_click=create_teleport)

    def rebuild_box():
        box.delete()
        ui.row().classes('src')
        tp.force_update()  # type: ignore

    ui.button('rebuild box', on_click=rebuild_box)

    screen.open('/')
    screen.click('create')
    screen.should_contain('Hello')
    screen.click('rebuild box')
    assert screen.find_by_css('.src > div').text == 'Hello'
