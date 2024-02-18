from typing import List

from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen


def test_open_close_dialog(screen: Screen):
    with ui.dialog() as d, ui.card():
        ui.label('Content')
        ui.button('Close', on_click=d.close)
    ui.button('Open', on_click=d.open)

    screen.open('/')
    screen.should_not_contain('Content')
    screen.click('Open')
    screen.wait(0.5)
    screen.should_contain('Content')
    screen.click('Close')
    screen.wait(0.5)
    screen.should_not_contain('Content')


def test_await_dialog(screen: Screen):
    with ui.dialog() as dialog, ui.card():
        ui.label('Are you sure?')
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit('Yes'))
            ui.button('No', on_click=lambda: dialog.submit('No'))

    async def show() -> None:
        results.append(await dialog)
    results: List[str] = []
    ui.button('Open', on_click=show)

    screen.open('/')
    screen.click('Open')
    screen.click('Yes')
    screen.click('Open')
    screen.click('No')
    screen.click('Open')
    screen.type(Keys.ESCAPE)
    screen.wait(0.5)
    assert results == ['Yes', 'No', None]
