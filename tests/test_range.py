from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_range(screen: SeleniumScreen):
    r = ui.range(min=0, max=100, value={'min': 20, 'max': 80})
    ui.label().bind_text_from(r, 'value', backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')

    screen.open('/')
    screen.should_contain('min: 20, max: 80')
