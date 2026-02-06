from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import SharedScreen


def test_editor(shared_screen: SharedScreen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.editor(placeholder='Type something here')
        ui.markdown().bind_content_from(editor, 'value', backward=lambda v: f'HTML code:\n```\n{v}\n```')

    shared_screen.open('/')
    shared_screen.find_element(editor).click()
    shared_screen.type('Hello\nworld!')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Hello<div>world!</div>')


def test_setting_value_twice(shared_screen: SharedScreen):
    # https://github.com/zauberzeug/nicegui/issues/3217
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.editor(value='X')
        ui.button('Reset').on_click(lambda: editor.set_value('X'))

    shared_screen.open('/')
    shared_screen.should_contain('X')

    shared_screen.find_element(editor).click()
    shared_screen.type(Keys.BACKSPACE + 'ABC')
    shared_screen.should_contain('ABC')

    shared_screen.click('Reset')
    shared_screen.should_contain('X')
