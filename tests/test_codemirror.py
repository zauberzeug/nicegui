import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen

# pylint: disable=protected-access


def test_codemirror(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror('Line 1\nLine 2\nLine 3')

    screen.open('/')
    screen.should_contain('Line 2')


def test_supported_values(screen: Screen):
    values: dict[str, list[str]] = {}

    @ui.page('/')
    def page():
        editor = ui.codemirror()

        async def fetch():
            values['languages'] = await editor.run_method('getLanguages')
            values['themes'] = await editor.run_method('getThemes')
            values['supported_themes'] = editor.supported_themes
            values['supported_languages'] = editor.supported_languages
            ui.label('Done')
        ui.button('Fetch', on_click=fetch)

    screen.open('/')
    screen.click('Fetch')
    screen.wait_for('Done')
    assert values['languages'] == values['supported_languages']
    assert values['themes'] == values['supported_themes']


@pytest.mark.parametrize('doc, sections, inserted, expected', [
    ('', [0, 1], [['A']], 'A'),
    ('', [0, 2], [['AB']], 'AB'),
    ('X', [1, 2], [['AB']], 'AB'),
    ('X', [1, -1], [], 'X'),
    ('X', [1, -1, 0, 1], [[], ['Y']], 'XY'),
    ('Hello', [5, -1, 0, 8], [[], [', world!']], 'Hello, world!'),
    ('Hello, world!', [5, -1, 7, 0, 1, -1], [], 'Hello!'),
    ('Hello, hello!', [2, -1, 3, 1, 4, -1, 3, 1, 1, -1], [[], ['y'], [], ['y']], 'Hey, hey!'),
    ('Hello, world!', [5, -1, 1, 3, 7, -1], [[], [' 🙂']], 'Hello 🙂 world!'),
    ('Hey! 🙂', [7, -1, 0, 4], [[], [' Ho!']], 'Hey! 🙂 Ho!'),
    ('Ha 🙂\nha 🙂', [3, -1, 2, 0, 4, -1, 2, 0], [[], [''], [], ['']], 'Ha \nha '),
])
def test_change_set(screen: Screen, doc: str, sections: list[int], inserted: list[list[str]], expected: str):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(doc)

    screen.open('/')
    assert editor._apply_change_set(sections, inserted) == expected


def test_set_value_preserves_cursor(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('Hello World')

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys(Keys.HOME)
    for _ in range(5):
        cm.send_keys(Keys.ARROW_RIGHT)  # Move cursor after 'Hello'

    editor.value = 'Hello Earth'
    screen.wait(0.5)

    cm.send_keys(',')  # Insert comma after 'Hello'
    screen.wait(0.5)

    assert editor.value == 'Hello, Earth'


def test_encode_codepoints():
    assert ui.codemirror._encode_codepoints('') == b''
    assert ui.codemirror._encode_codepoints('Hello') == bytes([1, 1, 1, 1, 1])
    assert ui.codemirror._encode_codepoints('🙂') == bytes([0, 1])
    assert ui.codemirror._encode_codepoints('Hello 🙂') == bytes([1, 1, 1, 1, 1, 1, 0, 1])
    assert ui.codemirror._encode_codepoints('😎😎😎') == bytes([0, 1, 0, 1, 0, 1])


def test_line_tooltip_api(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.codemirror('alpha\nbeta\ngamma').classes('w-24')
        ui.button('Set tooltip on line 2', on_click=lambda: editor.line_tooltips.__setitem__(2, 'debug'))
        ui.button('Set tooltip on line 3', on_click=lambda: editor.line_tooltips.__setitem__(3, 'info'))
        ui.button('Delete tooltip on line 3', on_click=lambda: editor.line_tooltips.__delitem__(3))
        ui.button('Update tooltips', on_click=lambda: editor.line_tooltips.update({2: 'warning'}))
        ui.button('Replace tooltips', on_click=lambda: setattr(editor, 'line_tooltips', {1: 'error'}))
        ui.button('Clear tooltips', on_click=lambda: editor.line_tooltips.clear())  # pylint: disable=unnecessary-lambda

    screen.open('/')
    screen.click('Set tooltip on line 2')
    ActionChains(screen.selenium).move_to_element(screen.find('beta')).perform()
    screen.should_contain('debug')

    screen.click('Set tooltip on line 3')
    ActionChains(screen.selenium).move_to_element(screen.find('gamma')).perform()
    screen.should_contain('info')

    screen.click('Delete tooltip on line 3')
    ActionChains(screen.selenium).move_to_element(screen.find('gamma')).perform()
    screen.wait(0.5)
    screen.should_not_contain('info')

    screen.click('Update tooltips')
    ActionChains(screen.selenium).move_to_element(screen.find('beta')).perform()
    screen.should_contain('warning')

    screen.click('Replace tooltips')
    ActionChains(screen.selenium).move_to_element(screen.find('alpha')).perform()
    screen.should_contain('error')
    ActionChains(screen.selenium).move_to_element(screen.find('beta')).perform()
    screen.wait(0.5)
    screen.should_not_contain('warning')

    screen.click('Clear tooltips')
    ActionChains(screen.selenium).move_to_element(screen.find('alpha')).perform()
    screen.wait(0.5)
    screen.should_not_contain('error')


def test_line_tooltip_stick_to_text(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.codemirror('abc').classes('w-24')
        editor.line_tooltips[1] = 'tooltip'

    screen.open('/')
    ActionChains(screen.selenium).move_to_element(screen.find('abc')).click().send_keys(Keys.HOME, Keys.ENTER).perform()
    ActionChains(screen.selenium).move_to_element(screen.find('abc')).perform()
    screen.should_contain('tooltip')


def test_line_tooltip_plain_text_default(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.codemirror('hello').classes('w-24')
        editor.line_tooltips[1] = 'a < b'

    screen.open('/')
    ActionChains(screen.selenium).move_to_element(screen.find('hello')).perform()
    screen.should_contain('a < b')  # The tooltip should render the text as-is, not interpret it as HTML.


def test_line_tooltip_html_sanitized(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.codemirror('hello', line_tooltip_html=True).classes('w-24')
        editor.line_tooltips[1] = '<b>bold</b><img src=x onerror="console.error(`X` + `SS`)">'

    screen.open('/')
    ActionChains(screen.selenium).move_to_element(screen.find('hello')).perform()
    screen.should_contain('bold')  # The tooltip should render the allowed HTML...
    assert 'XSS' not in screen.selenium.get_log('browser')  # ...but sanitize out any scripts.
