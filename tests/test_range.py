from nicegui import ui
from nicegui.testing import SharedScreen


def test_range(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        r = ui.range(min=0, max=100, value={'min': 20, 'max': 80})
        ui.label().bind_text_from(r, 'value', backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')

    shared_screen.open('/')
    shared_screen.should_contain('min: 20, max: 80')


def test_range_no_value(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        r = ui.range(min=0, max=100)
        ui.label().bind_text_from(r, 'value', backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')

    shared_screen.open('/')
    shared_screen.should_contain('min: 0, max: 100')
