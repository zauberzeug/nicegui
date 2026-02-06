from nicegui import ui
from nicegui.testing import SharedScreen


def test_open_close_expansion(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.expansion('Expansion') as e:
            ui.label('Content')
        ui.button('Open', on_click=e.open)
        ui.button('Close', on_click=e.close)

    shared_screen.open('/')
    shared_screen.should_contain('Expansion')
    shared_screen.should_not_contain('Content')

    shared_screen.click('Open')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Content')

    shared_screen.click('Close')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Content')


def test_caption(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.expansion('Expansion', caption='Caption'):
            ui.label('Content')

    shared_screen.open('/')
    shared_screen.should_contain('Expansion')
    shared_screen.should_contain('Caption')
    shared_screen.should_not_contain('Content')

    shared_screen.click('Expansion')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Expansion')
    shared_screen.should_contain('Caption')
    shared_screen.should_contain('Content')


def test_group(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.expansion('Expansion A', group='group'):
            ui.label('Content A')
        with ui.expansion('Expansion B', group='group'):
            ui.label('Content B')
        with ui.expansion('Expansion C', group='group'):
            ui.label('Content C')

    shared_screen.open('/')
    shared_screen.should_contain('Expansion A')
    shared_screen.should_contain('Expansion B')
    shared_screen.should_contain('Expansion C')
    shared_screen.should_not_contain('Content A')
    shared_screen.should_not_contain('Content B')
    shared_screen.should_not_contain('Content C')

    shared_screen.click('Expansion A')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Content A')
    shared_screen.should_not_contain('Content B')
    shared_screen.should_not_contain('Content C')

    shared_screen.click('Expansion B')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Content A')
    shared_screen.should_contain('Content B')
    shared_screen.should_not_contain('Content C')

    shared_screen.click('Expansion C')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Content A')
    shared_screen.should_not_contain('Content B')
    shared_screen.should_contain('Content C')
