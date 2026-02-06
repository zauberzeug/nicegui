from nicegui import ui
from nicegui.testing import SharedScreen


def test_carousel(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.carousel(arrows=True).props('control-color=primary'):
            for name in ['Alice', 'Bob', 'Carol']:
                with ui.carousel_slide():
                    ui.label(name).classes('w-32')

    shared_screen.open('/')
    shared_screen.should_contain('Alice')

    shared_screen.click('chevron_right')
    shared_screen.should_contain('Bob')

    shared_screen.click('chevron_right')
    shared_screen.should_contain('Carol')

    shared_screen.click('chevron_left')
    shared_screen.should_contain('Bob')

    shared_screen.click('chevron_left')
    shared_screen.should_contain('Alice')
