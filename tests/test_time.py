from nicegui import ui
from nicegui.testing import Screen


def test_time(screen: Screen):
    @ui.page('/')
    def page():
        t = ui.time(value='01:23')
        ui.label().bind_text_from(t, 'value')

    screen.open('/')
    screen.should_contain('01:23')
    screen.wait(0.2)
    screen.click('8')
    screen.should_contain('08:23')
    screen.wait(0.2)
    screen.click('45')
    screen.should_contain('08:45')
    screen.wait(0.2)
    screen.click('PM')
    screen.should_contain('20:45')
