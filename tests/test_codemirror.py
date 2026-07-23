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


def _diagnostic_count(screen: Screen, suffix: str = '') -> int:
    selector = f'.cm-lintRange{suffix}'
    return screen.selenium.execute_script(f'return document.querySelectorAll({selector!r}).length;')


def _lint_panel_present(screen: Screen) -> bool:
    return screen.selenium.execute_script("return document.querySelector('.cm-panel-lint') !== null;")


def test_diagnostics_property(screen: Screen):
    editor = None
    counts: dict[str, dict[str, int]] = {}

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('Line 1\nLine 2\nLine 3')

        async def snapshot(key: str):
            counts[key] = await editor.get_diagnostic_count()
            ui.label(f'snapshot-{key}')

        ui.button('SnapAfterSet', on_click=lambda: snapshot('after_set'))
        ui.button('SnapAfterClear', on_click=lambda: snapshot('after_clear'))

    screen.open('/')
    editor.diagnostics = [
        {'line': 1, 'message': 'oops', 'severity': 'error'},
        {'line': 3, 'message': 'note', 'severity': 'info'},
        {'line': 2, 'message': 'col mark', 'severity': 'warning', 'column': 2, 'end_column': 5},
    ]
    screen.wait_for(lambda: _diagnostic_count(screen) == 3)
    assert _diagnostic_count(screen, '-error') >= 1
    assert _diagnostic_count(screen, '-info') >= 1
    assert _diagnostic_count(screen, '-warning') >= 1

    # Column-targeted diagnostic must produce a sub-line mark.
    widths = screen.selenium.execute_script(
        "return Array.from(document.querySelectorAll('.cm-lintRange-warning'))"
        '.map(m => m.getBoundingClientRect().width);'
    )
    line_width = screen.selenium.execute_script(
        "const lines = document.querySelectorAll('.cm-line');"
        'return lines[1].getBoundingClientRect().width;'
    )
    assert widths and all(0 < w < line_width for w in widths)

    screen.click('SnapAfterSet')
    screen.wait_for('snapshot-after_set')
    assert counts['after_set'] == {'error': 1, 'warning': 1, 'info': 1, 'hint': 0, 'total': 3}

    editor.diagnostics = []
    screen.wait_for(lambda: _diagnostic_count(screen) == 0)

    screen.click('SnapAfterClear')
    screen.wait_for('snapshot-after_clear')
    assert counts['after_clear'] == {'error': 0, 'warning': 0, 'info': 0, 'hint': 0, 'total': 0}

    editor.diagnostics = [{'line': 2, 'message': 'no severity'}]
    screen.wait_for(lambda: _diagnostic_count(screen, '-error') == 1)

    editor.open_lint_panel()
    screen.wait_for(lambda: _lint_panel_present(screen))
    editor.close_lint_panel()
    screen.wait_for(lambda: not _lint_panel_present(screen))
    editor.toggle_lint_panel()
    screen.wait_for(lambda: _lint_panel_present(screen))
    editor.toggle_lint_panel()
    screen.wait_for(lambda: not _lint_panel_present(screen))


def test_diagnostic_message_default_is_plain_text(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    screen.open('/')
    editor.diagnostics = [
        {'line': 2, 'message': '<b>raw</b>'},
    ]
    screen.wait_for(lambda: _diagnostic_count(screen) == 1)
    editor.open_lint_panel()
    screen.wait_for(lambda: _lint_panel_present(screen))
    has_bold = screen.selenium.execute_script(
        'const p = document.querySelector(".cm-panel-lint");'
        'return !!(p && p.querySelector("b"));'
    )
    text = screen.selenium.execute_script(
        'const p = document.querySelector(".cm-panel-lint");'
        'return p ? p.textContent : "";'
    )
    assert not has_bold, 'default rendering must not interpret HTML'
    assert '<b>raw</b>' in text, 'default rendering shows raw tags as visible text'


def test_diagnostic_message_html_opt_in_renders_sanitized(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma', diagnostic_message_html=True)

    screen.open('/')
    editor.diagnostics = [
        {'line': 2, 'message': '<b>safe</b><script>window.__diag_hijack=1</script>'},
    ]
    screen.wait_for(lambda: _diagnostic_count(screen) == 1)
    editor.open_lint_panel()
    screen.wait_for(lambda: _lint_panel_present(screen))
    screen.wait_for(lambda: screen.selenium.execute_script(
        'const p = document.querySelector(".cm-panel-lint");'
        'return !!(p && p.querySelector("b"));'
    ))
    has_script = screen.selenium.execute_script(
        'const p = document.querySelector(".cm-panel-lint");'
        'return !!(p && p.querySelector("script"));'
    )
    hijacked = screen.selenium.execute_script('return window.__diag_hijack === 1')
    assert not has_script, 'DOMPurify should have stripped <script>'
    assert not hijacked, 'inline script must not have executed'


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
