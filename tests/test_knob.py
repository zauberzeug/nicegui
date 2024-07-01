from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_knob(screen: SeleniumScreen):
    knob = ui.knob(0.3, show_value=True)
    ui.button('turn up', on_click=lambda: knob.set_value(0.8))

    screen.open('/')
    screen.should_contain('0.3')
    screen.click('turn up')
    screen.should_contain('0.8')
