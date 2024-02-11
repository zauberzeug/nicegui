from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_open_close_expansion(screen: SeleniumScreen):
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


def test_caption(screen: SeleniumScreen):
    with ui.expansion('Expansion', caption='Caption'):
        ui.label('Content')

    screen.open('/')
    screen.should_contain('Expansion')
    screen.should_contain('Caption')
    screen.should_not_contain('Content')

    screen.click('Expansion')
    screen.wait(0.5)
    screen.should_contain('Expansion')
    screen.should_contain('Caption')
    screen.should_contain('Content')


def test_group(screen: SeleniumScreen):
    with ui.expansion('Expansion A', group='group'):
        ui.label('Content A')
    with ui.expansion('Expansion B', group='group'):
        ui.label('Content B')
    with ui.expansion('Expansion C', group='group'):
        ui.label('Content C')

    screen.open('/')
    screen.should_contain('Expansion A')
    screen.should_contain('Expansion B')
    screen.should_contain('Expansion C')
    screen.should_not_contain('Content A')
    screen.should_not_contain('Content B')
    screen.should_not_contain('Content C')

    screen.click('Expansion A')
    screen.wait(0.5)
    screen.should_contain('Content A')
    screen.should_not_contain('Content B')
    screen.should_not_contain('Content C')

    screen.click('Expansion B')
    screen.wait(0.5)
    screen.should_not_contain('Content A')
    screen.should_contain('Content B')
    screen.should_not_contain('Content C')

    screen.click('Expansion C')
    screen.wait(0.5)
    screen.should_not_contain('Content A')
    screen.should_not_contain('Content B')
    screen.should_contain('Content C')
