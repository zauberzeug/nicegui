from nicegui import ui
from nicegui.testing import Screen


def test_set_color_does_not_execute_javascript(screen: Screen):
    @ui.page('/')
    def page():
        with ui.button(icon='colorize'):
            picker = ui.color_picker()
        picker.set_color('ffffff" :x="document.title = \'XSS\'')

    screen.open('/')
    screen.click('colorize')
    screen.should_contain('HEX')
    screen.should_not_contain('XSS')
