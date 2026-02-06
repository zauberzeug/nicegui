from nicegui import ui
from nicegui.testing import SharedScreen


def test_time(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        t = ui.time(value='01:23')
        ui.label().bind_text_from(t, 'value')

    shared_screen.open('/')
    shared_screen.should_contain('01:23')
    shared_screen.wait(0.2)
    shared_screen.click('8')
    shared_screen.should_contain('08:23')
    shared_screen.wait(0.2)
    shared_screen.click('45')
    shared_screen.should_contain('08:45')
    shared_screen.wait(0.2)
    shared_screen.click('PM')
    shared_screen.should_contain('20:45')
