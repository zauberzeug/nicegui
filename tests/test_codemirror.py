import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from nicegui import ui
from nicegui.testing import Screen

# pylint: disable=protected-access


def _wait_for_cm_mount(screen: Screen) -> None:
    """Block until CM6 has inserted its contentDOM, proving the editor is ready for keydown dispatch."""
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


def test_keybinding_constructor(screen: Screen):
    """Bindings supplied via constructor fire on matching keystrokes."""
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(
            'hello',
            keybindings={
                'Mod-s': lambda e: events.append(f'save:{e.key}'),
                'F5': lambda: events.append('refresh'),
            },
        )

    screen.open('/')
    _wait_for_cm_mount(screen)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        'key: "s", code: "KeyS", ctrlKey: true, bubbles: true, cancelable: true,'
        '}));'
    )
    screen.wait_for(lambda: 'save:Mod-s' in events)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        'key: "F5", code: "F5", bubbles: true, cancelable: true,'
        '}));'
    )
    screen.wait_for(lambda: 'refresh' in events)


def test_keybinding_method(screen: Screen):
    """Bindings added via on_keybinding after construction fire correctly.

    Doubles as a runtime-reconfigure test (exercises the Vue watch + Compartment.reconfigure path).
    """
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello')
        editor.on_keybinding('Mod-r', lambda e: events.append(e.key))

    screen.open('/')
    _wait_for_cm_mount(screen)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        'key: "r", code: "KeyR", ctrlKey: true, bubbles: true, cancelable: true,'
        '}));'
    )
    screen.wait_for(lambda: 'Mod-r' in events)


def test_keybinding_replaces_existing(screen: Screen):
    """Re-binding the same key replaces the prior handler."""
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello', keybindings={'Mod-s': lambda: events.append('first')})
        editor.on_keybinding('Mod-s', lambda: events.append('second'))

    screen.open('/')
    _wait_for_cm_mount(screen)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        'key: "s", code: "KeyS", ctrlKey: true, bubbles: true, cancelable: true,'
        '}));'
    )
    screen.wait_for(lambda: 'second' in events)
    assert 'first' not in events, f'first handler should have been replaced, got {events}'


def test_keybinding_no_handler_no_traffic(screen: Screen):
    """No keybinding event traffic for a key that has no registered handler.

    Uses a positive-control binding (F2) to deterministically know the WS round-trip has completed.
    """
    events: list = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello', keybindings={'F2': lambda e: events.append({'key': e.key})})
        # Tap the raw channel to capture *any* keybinding traffic, including unmatched ones
        # if the JS dispatcher were buggy enough to emit them.
        editor.on('keybinding', lambda e: events.append(e.args))

    screen.open('/')
    _wait_for_cm_mount(screen)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        'key: "s", code: "KeyS", ctrlKey: true, bubbles: true, cancelable: true,'
        '}));'
    )
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        'key: "F2", code: "F2", bubbles: true, cancelable: true,'
        '}));'
    )
    # When the F2 event arrives, any Mod-s traffic would have arrived too (FIFO over WS).
    screen.wait_for(lambda: any(e.get('key') == 'F2' for e in events))
    assert not any(e.get('key') == 'Mod-s' for e in events), \
        f'expected no traffic for unbound Mod-s, got {events}'


def test_keybinding_prevent_default_false(screen: Screen):
    """A binding wrapped with prevent_default=False fires but does not call event.preventDefault()."""
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello', keybindings={
            'Mod-s': lambda e: events.append(e.key),
            'Mod-c': ui.codemirror.binding(lambda e: events.append(e.key), prevent_default=False),
        })

    screen.open('/')
    _wait_for_cm_mount(screen)

    default_prevented_s = screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'const ev = new KeyboardEvent("keydown", {'
        'key: "s", code: "KeyS", ctrlKey: true, bubbles: true, cancelable: true});'
        'el.editor.contentDOM.dispatchEvent(ev);'
        'return ev.defaultPrevented;'
    )
    screen.wait_for(lambda: 'Mod-s' in events)
    assert default_prevented_s is True, 'Mod-s should have called preventDefault'

    default_prevented_c = screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'const ev = new KeyboardEvent("keydown", {'
        'key: "c", code: "KeyC", ctrlKey: true, bubbles: true, cancelable: true});'
        'el.editor.contentDOM.dispatchEvent(ev);'
        'return ev.defaultPrevented;'
    )
    screen.wait_for(lambda: 'Mod-c' in events)
    assert default_prevented_c is False, 'Mod-c with prevent_default=False should not have called preventDefault'


def test_keybinding_per_os_fields_serialized(screen: Screen):
    """Per-OS overrides (mac/linux/win) surface in the keybindings prop sent to JS.

    We can't trigger CM6's per-OS keybinding resolution from a single Linux test runner,
    but we can verify the prop payload carries the right fields so CM6 will use them on
    each platform.
    """
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello', keybindings={
            'Alt-Down': ui.codemirror.binding(
                lambda: None, mac='Cmd-Down', linux='Ctrl-Down', win='Ctrl-Shift-Down',
            ),
            'F5': lambda: None,
        })

    screen.open('/')
    _wait_for_cm_mount(screen)
    bindings = screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'return el.$props.keybindings;'
    )
    by_key = {b['key']: b for b in bindings}
    assert by_key['Alt-Down'].get('mac') == 'Cmd-Down', f'expected mac field, got {by_key["Alt-Down"]}'
    assert by_key['Alt-Down'].get('linux') == 'Ctrl-Down', f'expected linux field, got {by_key["Alt-Down"]}'
    assert by_key['Alt-Down'].get('win') == 'Ctrl-Shift-Down', f'expected win field, got {by_key["Alt-Down"]}'
    for field in ('mac', 'linux', 'win'):
        assert field not in by_key['F5'], f'F5 should have no {field} field, got {by_key["F5"]}'


def test_remove_keybinding(screen: Screen):
    """remove_keybinding unbinds a key so subsequent presses produce no event."""
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello', keybindings={
            'Mod-s': lambda: events.append('save'),
            'F2': lambda e: events.append(f'control:{e.key}'),
        })
        editor.remove_keybinding('Mod-s')

    screen.open('/')
    _wait_for_cm_mount(screen)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        'key: "s", code: "KeyS", ctrlKey: true, bubbles: true, cancelable: true,'
        '}));'
    )
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        'key: "F2", code: "F2", bubbles: true, cancelable: true,'
        '}));'
    )
    screen.wait_for(lambda: 'control:F2' in events)
    assert 'save' not in events, f'expected Mod-s to be unbound, got {events}'
