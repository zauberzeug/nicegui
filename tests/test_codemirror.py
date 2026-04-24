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


def test_set_and_clear_line_tooltips_text(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    screen.open('/')
    screen.wait(0.3)
    editor.set_line_tooltips({2: {'severity': 'warning', 'message': 'maybe wrong'}})
    screen.wait(0.3)
    _trigger_hover(screen, editor, 2)
    screen.wait_for(lambda: 'maybe wrong' in (
        screen.selenium.execute_script('return document.querySelector(".cm-line-tooltip")?.textContent || ""') or ''))
    editor.clear_line_tooltips()
    screen.wait(0.3)


def test_line_tooltip_html_sanitized(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello\nworld')

    screen.open('/')
    screen.wait(0.3)
    # The `_html` value contains a <script> tag that DOMPurify must strip.
    editor.set_line_tooltips({1: {'_html': '<b>safe</b><script>window.__hijack=1</script>'}})
    screen.wait(0.3)
    _trigger_hover(screen, editor, 1)
    screen.wait_for(lambda: screen.selenium.execute_script(
        'const t = document.querySelector(".cm-line-tooltip");'
        'return !!(t && t.querySelector("b"));'
    ))
    has_script = screen.selenium.execute_script(
        'const t = document.querySelector(".cm-line-tooltip");'
        'return !!(t && t.querySelector("script"));'
    )
    hijacked = screen.selenium.execute_script('return window.__hijack === 1')
    assert not has_script, 'DOMPurify should have stripped <script>'
    assert not hijacked, 'inline script must not have executed'
