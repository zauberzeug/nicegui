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


def test_selection_change_event(screen: Screen):
    events: list[tuple[int, int]] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(
            'Line 1\nLine 2\nLine 3',
            on_selection_change=lambda e: events.append((e.line, e.column)),
        )

    screen.open('/')
    screen.should_contain('Line 2')
    # Move the cursor to line 2, column 4 (3 chars past line.from) via a CM6 selection transaction.
    # This bypasses focus/keystroke timing fragility in Selenium.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({selection: {anchor: el.editor.state.doc.line(2).from + 3}});'
    )
    screen.wait_for(lambda: (2, 4) in events)


def test_focus_change_event(screen: Screen):
    events: list[bool] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('Hello', on_focus_change=lambda e: events.append(e.focused))

    screen.open('/')
    screen.should_contain('Hello')
    # Focus then blur the editor via JS to avoid Selenium focus-stealing flakiness.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id}); el.editor.focus();'
    )
    screen.wait_for(lambda: True in events)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id}); el.editor.contentDOM.blur();'
    )
    screen.wait_for(lambda: False in events)


def test_viewport_change_event(screen: Screen):
    events: list[tuple[int, int]] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(
            '\n'.join(f'Line {i}' for i in range(1, 201)),
            on_viewport_change=lambda e: events.append((e.from_line, e.to_line)),
        )

    screen.open('/')
    screen.should_contain('Line 1')
    editor.reveal_line(150)
    # After reveal_line, the viewport should report a range containing line 150.
    screen.wait_for(lambda: any(from_line <= 150 <= to_line for from_line, to_line in events))


def test_geometry_change_event(screen: Screen):
    events: list[tuple[int, int, int]] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('Hello').classes('h-32')
        editor.on_geometry_change(lambda e: events.append((e.width, e.height, e.content_height)))

    screen.open('/')
    screen.should_contain('Hello')
    # Resize the editor's container to trigger a geometry change.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id}); el.$el.style.height = "400px";'
    )
    # Force CM to notice the size change.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id}); el.editor.requestMeasure();'
    )
    screen.wait_for(lambda: any(height >= 200 for _, height, _ in events))


def test_no_handler_no_traffic(screen: Screen):
    """Verify that dispatching a selection change emits NO event when no handler is registered.

    Subscribes to the raw 'selection-change' channel to detect any traffic; if the JS-side
    subscription gating works, the channel stays silent because the dispatcher bails before $emit.
    """
    events: list = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('Line 1\nLine 2\nLine 3')
        # Tap the raw event channel without going through on_selection_change so we
        # don't flip selection-tracking-enabled.
        editor.on('selection-change', lambda e: events.append(e.args))

    screen.open('/')
    screen.should_contain('Line 1')
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({selection: {anchor: el.editor.state.doc.line(2).from}});'
    )
    screen.wait(0.5)  # give any (incorrect) emit time to arrive
    assert events == [], f'expected no traffic without an on_selection_change handler, got {events}'


def test_debounce_override(screen: Screen):
    """Verify the debounce_ms override on the handler factory is honored by the JS dispatcher."""
    events: list[tuple[int, int]] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(
            'Line 1\nLine 2\nLine 3\nLine 4\nLine 5',
            on_selection_change=ui.codemirror.handler(
                lambda e: events.append((e.line, e.column)),
                debounce_ms=200,
            ),
        )

    screen.open('/')
    screen.should_contain('Line 1')
    # Fire 5 rapid selection moves well inside the 200 ms debounce window.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'for (let i = 1; i <= 5; i++) {'
        '  el.editor.dispatch({selection: {anchor: el.editor.state.doc.line(i).from}});'
        '}'
    )
    # Wait long enough for the trailing debounce to fire and any further frames to settle.
    screen.wait_for(lambda: len(events) >= 1)
    screen.wait(0.4)
    assert len(events) == 1, f'expected exactly one debounced event, got {events}'
    assert events[0][0] == 5, f'expected the trailing event on line 5, got {events[0]}'


def test_reveal_line(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('\n'.join(f'Line {i}' for i in range(1, 201)))

    screen.open('/')
    scroller = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-scroller")]')
    initial_top = screen.selenium.execute_script('return arguments[0].scrollTop', scroller)
    editor.reveal_line(150)
    screen.wait_for(lambda: screen.selenium.execute_script('return arguments[0].scrollTop', scroller) > initial_top)


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
