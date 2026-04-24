import pytest
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


def _line_decoration_count(screen: Screen, css_class: str) -> int:
    return screen.selenium.execute_script(
        f'return document.querySelectorAll(".cm-line.{css_class}").length;'
    )


def test_set_and_clear_line_decorations(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma\ndelta')

    screen.open('/')
    screen.wait(0.3)
    editor.set_decorations([
        {'kind': 'line', 'line': 1, 'class': 'my-line-class'},
        {'kind': 'line', 'line': 3, 'class': 'my-line-class'},
    ])
    screen.wait_for(lambda: _line_decoration_count(screen, 'my-line-class') == 2)
    editor.clear_decorations()
    screen.wait_for(lambda: _line_decoration_count(screen, 'my-line-class') == 0)


def test_named_decoration_sets_independent(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('one\ntwo\nthree')

    screen.open('/')
    screen.wait(0.3)
    editor.set_decorations([{'kind': 'line', 'line': 1, 'class': 'set-a'}], set_name='a')
    editor.set_decorations([{'kind': 'line', 'line': 2, 'class': 'set-b'}], set_name='b')
    screen.wait_for(lambda: _line_decoration_count(screen, 'set-a') == 1
                    and _line_decoration_count(screen, 'set-b') == 1)
    editor.clear_decorations('a')
    screen.wait_for(lambda: _line_decoration_count(screen, 'set-a') == 0
                    and _line_decoration_count(screen, 'set-b') == 1)


def test_highlight_lines_auto_clears(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('aa\nbb\ncc\ndd')

    screen.open('/')
    screen.wait(0.3)
    # Use a short duration to keep the test snappy.
    editor.highlight_lines([2, 4], css_class='cm-test-flash', duration_ms=200)
    screen.wait_for(lambda: _line_decoration_count(screen, 'cm-test-flash') == 2)
    screen.wait_for(lambda: _line_decoration_count(screen, 'cm-test-flash') == 0)


def test_highlight_lines_requires_css_class():
    import pytest as _pytest
    with _pytest.raises(TypeError):
        ui.codemirror.highlight_lines(ui.codemirror.__new__(ui.codemirror), [1])  # type: ignore[call-arg]
