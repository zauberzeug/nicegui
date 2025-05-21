from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen


def test_editor(screen: Screen):
    editor = ui.editor(placeholder='Type something here')
    ui.markdown().bind_content_from(editor, 'value', backward=lambda v: f'HTML code:\n```\n{v}\n```')

    screen.open('/')
    screen.find_element(editor).click()
    screen.type('Hello\nworld!')
    screen.wait(0.5)
    screen.should_contain('Hello<div>world!</div>')


def test_setting_value_twice(screen: Screen):
    # https://github.com/zauberzeug/nicegui/issues/3217
    editor = ui.editor(value='X')
    ui.button('Reset').on_click(lambda: editor.set_value('X'))

    screen.open('/')
    screen.should_contain('X')

    screen.find_element(editor).click()
    screen.type(Keys.BACKSPACE + 'ABC')
    screen.should_contain('ABC')

    screen.click('Reset')
    screen.should_contain('X')
