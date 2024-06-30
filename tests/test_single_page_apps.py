from nicegui import ui
from nicegui.testing import Screen


def test_routing_url(screen: Screen):
    @ui.outlet('/', on_navigate=lambda _: '/main')
    def layout():
        ui.label('main layout')
        yield

    @layout.view('/main')
    def main_content():
        ui.label('main content')

    screen.open('/')
    screen.should_contain('main layout')
    screen.should_contain('main content')
    assert '/main' in screen.selenium.current_url
