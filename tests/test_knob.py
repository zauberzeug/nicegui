from nicegui import ui
from nicegui.testing import SharedScreen


def test_knob(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        knob = ui.knob(0.3, show_value=True)
        ui.button('turn up', on_click=lambda: knob.set_value(0.8))

    shared_screen.open('/')
    shared_screen.should_contain('0.3')
    shared_screen.click('turn up')
    shared_screen.should_contain('0.8')
