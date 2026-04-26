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


def _trigger_hover(screen: Screen, editor, line_number: int) -> None:
    """Mimic a mouseover at the start of the given 1-indexed line so CM6's hoverTooltip fires."""
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        f'const pos = el.editor.state.doc.line({line_number}).from;'
        'const coords = el.editor.coordsAtPos(pos);'
        # CM6's hoverTooltip listens on the editor DOM. Dispatching synthetic mouseover/mousemove
        # events with the right clientX/clientY makes the underlying provider fire.
        'const target = el.editor.contentDOM;'
        'const init = {bubbles: true, clientX: coords.left + 2, clientY: (coords.top + coords.bottom) / 2};'
        'target.dispatchEvent(new MouseEvent("mouseover", init));'
        'target.dispatchEvent(new MouseEvent("mousemove", init));'
    )


def _tooltip_text(screen: Screen) -> str:
    return screen.selenium.execute_script(
        'return document.querySelector(".cm-tooltip-hover")?.textContent || ""') or ''


def _dismiss_hover(screen: Screen, editor) -> None:
    """Fire a mouseleave on the editor's contentDOM to dismiss any visible hover tooltip."""
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new MouseEvent("mouseleave", {bubbles: true}));'
    )


def test_set_and_clear_line_tooltips_text(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    screen.open('/')
    # Two named sets pinned to the same line — must merge on hover.
    editor.set_line_tooltips({2: {'severity': 'warning'}}, set_name='lint')
    editor.set_line_tooltips({2: {'origin': 'row-3'}}, set_name='source')
    _trigger_hover(screen, editor, 2)
    screen.wait_for(lambda: all(s in _tooltip_text(screen) for s in ['severity: warning', 'origin: row-3']))

    # Insert a line at the top via CM6 dispatch — 'beta' moves from line 2 to line 3,
    # and CM6's RangeSet.map() should carry the tooltip with it.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "zero\\n"}});'
    )
    _trigger_hover(screen, editor, 3)
    screen.wait_for(lambda: 'severity: warning' in _tooltip_text(screen))

    editor.clear_line_tooltips()
    _dismiss_hover(screen, editor)
    _trigger_hover(screen, editor, 3)
    screen.wait_for(lambda: screen.selenium.execute_script(
        'return document.querySelector(".cm-tooltip-hover") === null'))


def test_line_tooltip_html_sanitized(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello\nworld')

    screen.open('/')
    # The `_html` value contains a <script> tag and an inline event handler. DOMPurify must
    # strip both. The <b> tag should survive. SVG onload is used (rather than img onerror) so
    # the test does not trigger a stray network fetch — that would surface as a console error
    # during teardown even though the handler itself was successfully stripped.
    editor.set_line_tooltips({1: {'_html': '<b>safe</b><script>window.__hijack=1</script>'
                                           '<svg onload="window.__hijack2=1"></svg>'}})
    _trigger_hover(screen, editor, 1)
    screen.wait_for(lambda: screen.selenium.execute_script(
        'const t = document.querySelector(".cm-tooltip-hover");'
        'return !!(t && t.querySelector("b"));'
    ))
    has_script = screen.selenium.execute_script(
        'const t = document.querySelector(".cm-tooltip-hover");'
        'return !!(t && t.querySelector("script"));'
    )
    hijacked = screen.selenium.execute_script('return window.__hijack === 1')
    onload_hijacked = screen.selenium.execute_script('return window.__hijack2 === 1')
    assert not has_script, 'DOMPurify should have stripped <script>'
    assert not hijacked, 'inline script must not have executed'
    assert not onload_hijacked, 'inline event handler must be stripped'
