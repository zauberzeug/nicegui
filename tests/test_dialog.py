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
        ui.button('Yes', on_click=lambda: dialog.submit('Yes'))
        ui.button('No', on_click=lambda: dialog.submit('No'))

    async def show() -> None:
        ui.notify(f'Result: {await dialog}')

    ui.button('Open', on_click=show)

    screen.open('/')
    screen.click('Open')
    screen.wait(0.2)
    screen.click('Yes')
    screen.should_contain('Result: Yes')

    screen.click('Open')
    screen.wait(0.2)
    screen.click('No')
    screen.should_contain('Result: No')

    screen.click('Open')
    screen.type(Keys.ESCAPE)
    screen.should_contain('Result: None')


def test_dialog_scroll_behavior(screen: Screen):
    ui.add_css('html { scroll-behavior: smooth }')
    ui.link('Go to bottom', '#bottom')
    ui.link_target('bottom').classes('mt-[2000px]')
    ui.button('dialog', on_click=lambda: ui.dialog(value=True))

    screen.open('/')
    screen.click('Go to bottom')
    screen.wait(1)
    position = screen.selenium.execute_script('return window.scrollY')
    assert position > 1000

    screen.click('dialog')
    screen.wait(0.5)
    screen.type(Keys.ESCAPE)
    screen.wait(0.2)
    assert screen.selenium.execute_script('return window.scrollY') == position
