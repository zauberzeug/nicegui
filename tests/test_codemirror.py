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


def test_custom_completions_initialization(screen: Screen):
    """Test that custom_completions can be passed during initialization."""
    completions = [
        {'label': 'test_func', 'detail': '()', 'type': 'function'},
        {'label': 'test_var', 'detail': 'str', 'type': 'variable'},
    ]

    @ui.page('/')
    def page():
        editor = ui.codemirror('', custom_completions=completions)
        ui.label(f'Completions: {len(editor.custom_completions)}')

    screen.open('/')
    screen.should_contain('Completions: 2')


def test_custom_completions_property(screen: Screen):
    """Test the custom_completions property getter and setter."""
    editor_ref = []

    @ui.page('/')
    def page():
        editor = ui.codemirror('')
        editor_ref.append(editor)

        def update_completions():
            editor.custom_completions = [
                {'label': 'new_func', 'type': 'function'},
            ]
            ui.label(f'Updated: {len(editor.custom_completions)}')

        ui.button('Update', on_click=update_completions)

    screen.open('/')
    assert editor_ref[0].custom_completions == []
    screen.click('Update')
    screen.should_contain('Updated: 1')


def test_set_completions_method(screen: Screen):
    """Test the set_completions() method."""
    editor_ref = []

    @ui.page('/')
    def page():
        editor = ui.codemirror('')
        editor_ref.append(editor)

        def set_math():
            editor.set_completions(
                [
                    {'label': 'math.sin', 'detail': '(x)', 'type': 'function'},
                    {'label': 'math.cos', 'detail': '(x)', 'type': 'function'},
                ]
            )
            ui.label('Math completions set')

        def clear():
            editor.set_completions([])
            ui.label('Cleared')

        ui.button('Set Math', on_click=set_math)
        ui.button('Clear', on_click=clear)

    screen.open('/')
    assert editor_ref[0].custom_completions == []

    screen.click('Set Math')
    screen.should_contain('Math completions set')
    assert len(editor_ref[0].custom_completions) == 2

    screen.click('Clear')
    screen.should_contain('Cleared')
    assert editor_ref[0].custom_completions == []


def test_custom_completions_with_none(screen: Screen):
    """Test that None is handled gracefully for custom_completions."""
    editor_ref = []

    @ui.page('/')
    def page():
        editor = ui.codemirror('', custom_completions=None)
        editor_ref.append(editor)

    screen.open('/')
    screen.wait(0.2)
    assert editor_ref[0].custom_completions == []
    editor_ref[0].set_completions(None)
    assert editor_ref[0].custom_completions == []


def test_cursor_line_event(screen: Screen):
    """Test that on_cursor_line fires with a 1-indexed line number when the cursor moves."""
    lines: list[int] = []

    @ui.page('/')
    def page():
        ui.codemirror('Line 1\nLine 2\nLine 3', on_cursor_line=lambda e: lines.append(e.args['line']))

    screen.open('/')
    cm = screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content')
    cm.click()
    cm.send_keys(Keys.CONTROL, Keys.HOME)
    cm.send_keys(Keys.ARROW_DOWN)
    screen.wait_for(lambda: 2 in lines)
    cm.send_keys(Keys.ARROW_DOWN)
    screen.wait_for(lambda: 3 in lines)


def test_save_event(screen: Screen):
    """Test that on_save fires when the user presses Ctrl+S."""
    saved: list[bool] = []

    @ui.page('/')
    def page():
        ui.codemirror('content', on_save=lambda _: saved.append(True))

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys(Keys.CONTROL, 's')
    screen.wait(0.3)
    assert saved == [True]


def test_decorations(screen: Screen):
    """Test setting and clearing line decorations."""
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('Line 1\nLine 2\nLine 3')

    screen.open('/')
    screen.wait(0.3)
    editor.run_method('setDecorations', {'highlight': [{'kind': 'line', 'line': 2, 'class': 'cm-highlighted'}]})
    screen.wait(0.3)
    # A line-level decoration results in a cm-highlighted class on a line element.
    highlighted = screen.selenium.find_elements(By.CSS_SELECTOR, '.cm-highlighted')
    assert len(highlighted) >= 1

    editor.run_method('setDecorations', {'highlight': []})
    screen.wait(0.3)
    highlighted = screen.selenium.find_elements(By.CSS_SELECTOR, '.cm-highlighted')
    assert len(highlighted) == 0


def test_highlight_lines(screen: Screen):
    """Test highlight_lines applies a temporary line class and removes it after the duration."""
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('A\nB\nC')

    screen.open('/')
    screen.wait(0.3)
    editor.highlight_lines([1], css_class='cm-flash', duration_ms=500)
    screen.wait(0.1)
    assert screen.selenium.find_elements(By.CSS_SELECTOR, '.cm-flash')
    screen.wait(0.7)
    assert not screen.selenium.find_elements(By.CSS_SELECTOR, '.cm-flash')


def test_set_diagnostics(screen: Screen):
    """Test that set_diagnostics installs lint markers in the editor."""
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('foo\nbar\nbaz')

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.find_elements(By.CSS_SELECTOR, '.cm-content'))
    editor.set_diagnostics([
        {'line': 2, 'message': 'suspicious name', 'severity': 'warning'},
    ])
    # Diagnostics render as .cm-lintRange spans once the linter processes them.
    screen.wait_for(lambda: len(screen.selenium.find_elements(By.CSS_SELECTOR, '.cm-lintRange')) >= 1)


def test_reveal_line(screen: Screen):
    """Test that reveal_line scrolls a line into view without error."""
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('\n'.join(f'line {i}' for i in range(1, 201)))

    screen.open('/')
    screen.wait(0.3)
    editor.reveal_line(150)
    screen.wait(0.3)
    # The revealed line should be visible on screen.
    content = screen.selenium.execute_script('''
        const els = document.querySelectorAll('.cm-line');
        for (const el of els) {
          if (el.textContent === 'line 150') {
            const rect = el.getBoundingClientRect();
            return rect.top >= 0 && rect.bottom <= window.innerHeight;
          }
        }
        return false;
    ''')
    assert content
