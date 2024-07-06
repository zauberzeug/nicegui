from nicegui import ui
from nicegui.testing import Screen


def test_changing_options(screen: Screen):
    r = ui.radio([10, 20, 30], value=10)
    ui.label().bind_text_from(r, 'value', lambda v: f'value = {v}')
    ui.button('reverse', on_click=lambda: (r.options.reverse(), r.update()))
    ui.button('clear', on_click=lambda: (r.options.clear(), r.update()))

    screen.open('/')
    screen.click('reverse')
    screen.should_contain('value = 10')
    screen.click('clear')
    screen.should_contain('value = None')
