from nicegui import ui
from nicegui.testing import Screen


def test_fab(screen: Screen):
    with ui.fab('menu', label='FAB') as fab:
        ui.fab_action('info', label='Action 1', on_click=lambda: ui.notify('Action 1 clicked'))
        ui.fab_action('info', label='Action 2', on_click=lambda: ui.notify('Action 2 clicked'), auto_close=False)

    ui.button('Open FAB', on_click=fab.open)
    ui.button('Close FAB', on_click=fab.close)
    ui.button('Toggle FAB', on_click=fab.toggle)
    ui.label().bind_text_from(fab, 'value', lambda v: 'FAB is open' if v else 'FAB is closed')

    screen.open('/')
    screen.click('FAB')
    screen.click('Action 1')
    screen.should_contain('Action 1 clicked')
    screen.should_contain('FAB is closed')

    screen.click('FAB')
    screen.click('Action 2')
    screen.should_contain('Action 2 clicked')
    screen.should_contain('FAB is open')

    screen.click('Close FAB')
    screen.should_contain('FAB is closed')

    screen.click('Open FAB')
    screen.should_contain('FAB is open')

    screen.click('Toggle FAB')
    screen.should_contain('FAB is closed')

    screen.click('Toggle FAB')
    screen.should_contain('FAB is open')
