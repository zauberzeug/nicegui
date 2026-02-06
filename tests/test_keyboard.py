from nicegui import ui
from nicegui.testing import SharedScreen


def test_keyboard(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        result = ui.label()
        ui.keyboard(on_key=lambda e: result.set_text(f'{e.key, e.action}'))

    shared_screen.open('/')
    shared_screen.wait(1.0)
    shared_screen.type('t')
    shared_screen.should_contain('t, KeyboardAction(keydown=False, keyup=True, repeat=False)')
