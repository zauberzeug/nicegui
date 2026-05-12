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


def _wait_for_editor(screen: Screen) -> None:
    screen.wait_for(lambda: screen.selenium.find_elements(By.CSS_SELECTOR, '.cm-content'))


def test_line_anchors_populates_mirror(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = [{'id': 'a1', 'line': 2}, {'id': 'a2', 'line': 4}]
    screen.wait_for(lambda: editor.line_anchor_positions == {'a1': 2, 'a2': 4})


def test_line_anchors_replace_and_clear(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = [{'id': 'x', 'line': 1}, {'id': 'y', 'line': 2}]
    screen.wait_for(lambda: editor.line_anchor_positions == {'x': 1, 'y': 2})
    editor.line_anchors = [{'id': 'z', 'line': 3}]
    screen.wait_for(lambda: editor.line_anchor_positions == {'z': 3})
    editor.line_anchors = []
    screen.wait_for(lambda: editor.line_anchor_positions == {})


def test_clear_after_typing_does_not_resurrect_anchors(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = [{'id': 'mid', 'line': 3}]
    screen.wait_for(lambda: editor.line_anchor_positions.get('mid') == 3)
    # The pending JS debounce timer plus the explicit clear must converge to an
    # empty mirror — a stale late-fire emit must not resurrect the cleared anchor.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    editor.line_anchors = []
    screen.wait_for(lambda: editor.line_anchor_positions == {})
    screen.wait(0.2)
    assert editor.line_anchor_positions == {}


def test_anchor_remap_on_edit(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = [{'id': 'mid', 'line': 3}]
    screen.wait_for(lambda: editor.line_anchor_positions.get('mid') == 3)
    # Insert a new line at the very start; line 3 should remap to line 4.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    screen.wait_for(lambda: editor.line_anchor_positions.get('mid') == 4)


def test_anchor_emissions_bounded_during_typing(screen: Screen):
    editor = None
    emissions: list[dict] = []

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello\nworld\n!')
        editor.on('anchor-positions', lambda e: emissions.append(e.args))

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = [{'id': 'a', 'line': 1}, {'id': 'b', 'line': 3}]
    screen.wait_for(lambda: editor.line_anchor_positions == {'a': 1, 'b': 3})
    emissions.clear()
    # Dispatch 10 doc changes synchronously from JS so they all land within the 50ms debounce
    # window, regardless of Selenium IPC speed. With coalescing we expect a single emission.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'for (let i = 0; i < 10; i++) el.editor.dispatch({changes: {from: 0, insert: "x"}});'
    )
    screen.wait(0.2)
    assert len(emissions) == 1, f'expected one coalesced emission for 10 synchronous edits, got {len(emissions)}'
