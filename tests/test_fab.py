from nicegui import ui
from nicegui.testing import Screen


def test_fab(screen: Screen):
    with ui.fab('menu', label='fab'):
        ui.fab_action('info', text='Action 1')
        ui.fab_action('info', text='Action 2')
        ui.fab_action('info', text='Action 3')

    screen.open('/')
    screen.click('fab')
    screen.should_contain('Action 1')
