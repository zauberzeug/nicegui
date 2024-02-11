from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_keyboard(screen: SeleniumScreen):
    result = ui.label()
    ui.keyboard(on_key=lambda e: result.set_text(f'{e.key, e.action}'))

    screen.open('/')
    screen.wait(1.0)
    screen.type('t')
    screen.should_contain('t, KeyboardAction(keydown=False, keyup=True, repeat=False)')
