from nicegui import ui
from nicegui.testing import SharedScreen


def test_fab(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.fab('menu', label='FAB') as fab:
            ui.fab_action('info', label='Action 1', on_click=lambda: ui.notify('Action 1 clicked'))
            ui.fab_action('info', label='Action 2', on_click=lambda: ui.notify('Action 2 clicked'), auto_close=False)

        ui.button('Open FAB', on_click=fab.open)
        ui.button('Close FAB', on_click=fab.close)
        ui.button('Toggle FAB', on_click=fab.toggle)
        ui.label().bind_text_from(fab, 'value', lambda v: 'FAB is open' if v else 'FAB is closed')

    shared_screen.open('/')
    shared_screen.click('FAB')
    shared_screen.click('Action 1')
    shared_screen.should_contain('Action 1 clicked')
    shared_screen.should_contain('FAB is closed')

    shared_screen.click('FAB')
    shared_screen.click('Action 2')
    shared_screen.should_contain('Action 2 clicked')
    shared_screen.should_contain('FAB is open')

    shared_screen.click('Close FAB')
    shared_screen.should_contain('FAB is closed')

    shared_screen.click('Open FAB')
    shared_screen.should_contain('FAB is open')

    shared_screen.click('Toggle FAB')
    shared_screen.should_contain('FAB is closed')

    shared_screen.click('Toggle FAB')
    shared_screen.should_contain('FAB is open')
