from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen


def test_editor(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.editor(placeholder='Type something here')
        ui.markdown().bind_content_from(editor, 'value', backward=lambda v: f'HTML code:\n```\n{v}\n```')

    screen.open('/')
    screen.find_element(editor).click()
    screen.type('Hello\nworld!')
    screen.should_contain('Hello<div>world!</div>')


def test_setting_value_twice(screen: Screen):
    # https://github.com/zauberzeug/nicegui/issues/3217
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.editor(value='X')
        ui.button('Reset').on_click(lambda: editor.set_value('X'))

    screen.open('/')
    screen.should_contain('X')

    screen.find_element(editor).click()
    screen.type(Keys.BACKSPACE + 'ABC')
    screen.should_contain('ABC')

    screen.click('Reset')
    screen.should_contain('X')


def test_sanitize(screen: Screen):
    def payload(message: str) -> str:
        return f'<img src=x onerror=Quasar.Notify.create({{message:"{message}",timeout:0}})>'

    @ui.page('/')
    def page():
        ui.editor(value=payload('Alpha'), sanitize=False)
        ui.editor(value=payload('Bravo'))
        unsafe_editor = ui.editor(sanitize=False)
        safe_editor = ui.editor()

        def update() -> None:
            unsafe_editor.set_value(payload('Charlie'))
            safe_editor.set_value(payload('Delta'))
        ui.button('Update', on_click=update)

    screen.allowed_js_errors.append('/x - Failed to load resource')
    screen.open('/')
    screen.should_contain('Alpha')
    screen.click('Update')
    screen.should_contain('Charlie')
    screen.should_not_contain('Bravo')
    screen.should_not_contain('Delta')
    assert sum(img.get_attribute('onerror') is not None for img in screen.find_all_by_tag('img')) == 2
