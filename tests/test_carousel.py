from nicegui import ui
from nicegui.testing import Screen


def test_carousel(screen: Screen):
    @ui.page('/')
    def page():
        with ui.carousel(arrows=True).props('control-color=primary'):
            for name in ['Alice', 'Bob', 'Carol']:
                with ui.carousel_slide():
                    ui.label(name).classes('w-32')

    screen.open('/')
    screen.should_contain('Alice')

    screen.click('chevron_right')
    screen.should_contain('Bob')

    screen.click('chevron_right')
    screen.should_contain('Carol')

    screen.click('chevron_left')
    screen.should_contain('Bob')

    screen.click('chevron_left')
    screen.should_contain('Alice')
