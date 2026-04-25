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


def test_set_line_anchors_initial_mirror(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne')

    screen.open('/')
    screen.wait(0.3)
    editor.set_line_anchors([{'id': 'a1', 'line': 2}, {'id': 'a2', 'line': 4}])
    # Mirror is updated synchronously before any JS round-trip
    assert editor.line_anchor_positions == {'default': {'a1': 2, 'a2': 4}}


def test_clear_line_anchors_named_and_all(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc')

    screen.open('/')
    screen.wait(0.3)
    editor.set_line_anchors([{'id': 'x', 'line': 1}], set_name='breakpoints')
    editor.set_line_anchors([{'id': 'y', 'line': 2}], set_name='targets')
    assert set(editor.line_anchor_positions.keys()) == {'breakpoints', 'targets'}
    editor.clear_line_anchors('breakpoints')
    assert set(editor.line_anchor_positions.keys()) == {'targets'}
    editor.clear_line_anchors()
    assert editor.line_anchor_positions == {}


def test_anchor_remap_on_edit(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne')

    screen.open('/')
    screen.wait(0.3)
    editor.set_line_anchors([{'id': 'mid', 'line': 3}])
    screen.wait(0.3)  # let setLineAnchors round-trip and populate the anchorField
    # Insert a new line at the very start; line 3 should remap to line 4.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    screen.wait_for(lambda: editor.line_anchor_positions.get('default', {}).get('mid') == 4)


def test_set_line_anchors_rejects_invalid_input(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc')

    screen.open('/')
    with pytest.raises(ValueError):
        editor.set_line_anchors([{'id': 'x', 'line': 0}])
    with pytest.raises(ValueError):
        editor.set_line_anchors([{'id': 'x', 'line': -1}])
    with pytest.raises(ValueError):
        editor.set_line_anchors([{'id': 'dup', 'line': 1}, {'id': 'dup', 'line': 2}])


def test_anchor_emissions_bounded_during_typing(screen: Screen):
    editor = None
    emissions: list[dict] = []

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello\nworld\n!')
        editor.on('anchor-positions', lambda e: emissions.append(e.args))

    screen.open('/')
    screen.wait(0.3)
    editor.set_line_anchors([{'id': 'a', 'line': 1}, {'id': 'b', 'line': 3}])
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys(Keys.END)
    for ch in 'abcdefghij':  # ten keystrokes
        cm.send_keys(ch)
    screen.wait(0.2)  # let the 50 ms debounce settle
    # 10 keystrokes through a 50 ms debounce should not produce one event per keystroke.
    # The threshold is loose so the test stays green on slower CI (where send_keys cadence
    # exceeds the debounce window); the point is coalescing happens, not the exact count.
    assert len(emissions) < 10, f'expected coalescing (<10 emissions for 10 keystrokes), got {len(emissions)}'
