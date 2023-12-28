from nicegui import ui
from nicegui.testing import Screen


def test_open_close_expansion(screen: Screen):
    with ui.expansion('Expansion') as e:
        ui.label('Content')
    ui.button('Open', on_click=e.open)
    ui.button('Close', on_click=e.close)

    screen.open('/')
    screen.should_contain('Expansion')
    screen.should_not_contain('Content')
    screen.click('Open')
    screen.wait(0.5)
    screen.should_contain('Content')
    screen.click('Close')
    screen.wait(0.5)
    screen.should_not_contain('Content')
