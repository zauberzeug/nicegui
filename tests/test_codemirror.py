import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from nicegui import ui
from nicegui.testing import Screen

# pylint: disable=protected-access


def _wait_for_cm_mount(screen: Screen) -> None:
    WebDriverWait(screen.selenium, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.cm-content'))
    )


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
    _wait_for_cm_mount(screen)
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
    _wait_for_cm_mount(screen)
    editor.set_decorations([{'kind': 'line', 'line': 1, 'class': 'set-a'}], set_name='a')
    editor.set_decorations([{'kind': 'line', 'line': 2, 'class': 'set-b'}], set_name='b')
    screen.wait_for(lambda: _line_decoration_count(screen, 'set-a') == 1
                    and _line_decoration_count(screen, 'set-b') == 1)
    editor.clear_decorations('a')
    screen.wait_for(lambda: _line_decoration_count(screen, 'set-a') == 0
                    and _line_decoration_count(screen, 'set-b') == 1)


def _visible_text_length(screen: Screen) -> int:
    return screen.selenium.execute_script(
        'return document.querySelector(".cm-content").innerText.length;'
    )


def _replacement_widget_count(screen: Screen, css_class: str) -> int:
    return screen.selenium.execute_script(
        f'return document.querySelectorAll(".cm-content span.{css_class}").length;'
    )


def test_replace_decoration_collapses_range(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    screen.open('/')
    _wait_for_cm_mount(screen)
    baseline = _visible_text_length(screen)
    # 'beta\n' spans offsets 6..11 (5 chars + newline) — collapse hides those characters.
    editor.set_decorations([{'kind': 'replace', 'from': 6, 'to': 11}])
    screen.wait_for(lambda: _visible_text_length(screen) < baseline)
    editor.clear_decorations()
    screen.wait_for(lambda: _visible_text_length(screen) == baseline)


def test_replace_decoration_with_text(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    screen.open('/')
    _wait_for_cm_mount(screen)
    editor.set_decorations([
        {'kind': 'replace', 'from': 6, 'to': 10, 'text': 'BETA-NEW', 'class': 'cm-test-suggest'},
    ])
    screen.wait_for(lambda: _replacement_widget_count(screen, 'cm-test-suggest') == 1)
    widget_text = screen.selenium.execute_script(
        'return document.querySelector(".cm-content span.cm-test-suggest").textContent;'
    )
    assert widget_text == 'BETA-NEW'
    # Document is unchanged — the editor's value must still contain the original text.
    assert 'beta' in editor.value
    assert 'BETA-NEW' not in editor.value


def test_widget_text_renders_html_sanitized(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    screen.open('/')
    _wait_for_cm_mount(screen)
    editor.set_decorations([
        {'kind': 'widget', 'position': 5,
         'text': '<b>safe</b><script>window.__deco_hijack=1</script>',
         'class': 'cm-test-html-widget'},
    ])
    screen.wait_for(lambda: screen.selenium.execute_script(
        'const w = document.querySelector(".cm-content span.cm-test-html-widget");'
        'return !!(w && w.querySelector("b"));'
    ))
    has_script = screen.selenium.execute_script(
        'const w = document.querySelector(".cm-content span.cm-test-html-widget");'
        'return !!(w && w.querySelector("script"));'
    )
    hijacked = screen.selenium.execute_script('return window.__deco_hijack === 1')
    assert not has_script, 'DOMPurify should have stripped <script>'
    assert not hijacked, 'inline script must not have executed'


def test_replace_decoration_block_mode(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma\ndelta')

    screen.open('/')
    _wait_for_cm_mount(screen)
    # Lines 2-3 ('beta\ngamma') span offsets 6..16 — must cover full lines for block mode.
    editor.set_decorations([{
        'kind': 'replace', 'from': 6, 'to': 16,
        'text': '{ ... folded ... }', 'class': 'cm-test-fold', 'block': True,
    }])
    screen.wait_for(lambda: _replacement_widget_count(screen, 'cm-test-fold') == 1)
    visible = screen.selenium.execute_script(
        'return document.querySelector(".cm-content").innerText;'
    )
    assert 'beta' not in visible
    assert 'gamma' not in visible
    assert '{ ... folded ... }' in visible


def test_mark_decoration_styles_range(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    screen.open('/')
    _wait_for_cm_mount(screen)
    editor.set_decorations([{
        'kind': 'mark', 'from': 6, 'to': 10,
        'class': 'cm-test-mark', 'attributes': {'data-marker': 'beta'},
    }])
    screen.wait_for(lambda: _replacement_widget_count(screen, 'cm-test-mark') == 1)
    marker_attr = screen.selenium.execute_script(
        'return document.querySelector(".cm-content span.cm-test-mark").getAttribute("data-marker");'
    )
    assert marker_attr == 'beta'
    assert editor.value == 'alpha\nbeta\ngamma'
    editor.clear_decorations()
    screen.wait_for(lambda: _replacement_widget_count(screen, 'cm-test-mark') == 0)


def test_widget_decoration_inserts_text(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    screen.open('/')
    _wait_for_cm_mount(screen)
    editor.set_decorations([
        {'kind': 'widget', 'position': 5, 'text': '<-- end of alpha', 'class': 'cm-test-hint'},
    ])
    screen.wait_for(lambda: _replacement_widget_count(screen, 'cm-test-hint') == 1)
    widget_text = screen.selenium.execute_script(
        'return document.querySelector(".cm-content span.cm-test-hint").textContent;'
    )
    assert widget_text == '<-- end of alpha'
    # Document is unchanged — widgets are presentation only.
    assert editor.value == 'alpha\nbeta\ngamma'
