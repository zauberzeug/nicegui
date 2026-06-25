import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from nicegui import ui
from nicegui.testing import Screen

# pylint: disable=protected-access

# CodeMirror resolves 'Mod' to Cmd on macOS and Ctrl elsewhere, so synthesized keydowns must use the
# matching modifier or the keybinding tests fail for Mac devs while passing on the Linux CI runner.
# Mirror CM6's own platform check as a computed property name (resolves to ctrlKey on Linux, metaKey on Mac).
_MOD_KEY_JS = '[/Mac/.test(navigator.platform) ? "metaKey" : "ctrlKey"]: true'


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
    """Bindings supplied via constructor fire on matching keystrokes and override basicSetup defaults."""
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
                'Mod-z': lambda e: events.append(f'override:{e.key}'),
            },
        )

    screen.open('/')
    _wait_for_cm_mount(screen)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        f'key: "s", code: "KeyS", {_MOD_KEY_JS}, bubbles: true, cancelable: true,'
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

    # Mod-z is a basicSetup default (undo) — verify the user binding wins via Prec.high
    # in setupExtensions(). Pre-seed undo history so a regression would actually undo something.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: el.editor.state.doc.length, insert: "after"}});'
    )
    screen.wait_for(lambda: editor.value == 'helloafter')

    doc_after_z = screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        f'key: "z", code: "KeyZ", {_MOD_KEY_JS}, bubbles: true, cancelable: true,'
        '}));'
        'return el.editor.state.doc.toString();'
    )
    screen.wait_for(lambda: 'override:Mod-z' in events)
    assert doc_after_z == 'helloafter', \
        f'basicSetup undo should have been overridden, doc is {doc_after_z!r}'


def test_keybinding_method(screen: Screen):
    """Bindings added via on_keybinding after mount fire correctly and win over basicSetup defaults.

    Exercises the Vue watch + Compartment.reconfigure path AND verifies Prec.high persists
    across reconfigure (Mod-z is basicSetup's undo).
    """
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello')

    screen.open('/')
    _wait_for_cm_mount(screen)

    # Pre-seed undo history so a Prec.high regression would actually undo something.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: el.editor.state.doc.length, insert: "after"}});'
    )
    screen.wait_for(lambda: editor.value == 'helloafter')

    # Bind AFTER mount — exercises the watcher + Compartment.reconfigure path.
    editor.on_keybinding('Mod-z', lambda e: events.append(e.key))
    WebDriverWait(screen.selenium, 5).until(
        lambda d: d.execute_script(
            f'const el = getElement({editor.id});'
            'return (el.$props.keybindings || []).some(b => b.key === "Mod-z");'
        )
    )

    doc_after_z = screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        f'key: "z", code: "KeyZ", {_MOD_KEY_JS}, bubbles: true, cancelable: true,'
        '}));'
        'return el.editor.state.doc.toString();'
    )
    screen.wait_for(lambda: 'Mod-z' in events)
    assert doc_after_z == 'helloafter', \
        f'basicSetup undo should have been overridden after reconfigure, doc is {doc_after_z!r}'


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
        f'key: "s", code: "KeyS", {_MOD_KEY_JS}, bubbles: true, cancelable: true,'
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
        f'key: "s", code: "KeyS", {_MOD_KEY_JS}, bubbles: true, cancelable: true,'
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
        f'key: "s", code: "KeyS", {_MOD_KEY_JS}, bubbles: true, cancelable: true}});'
        'el.editor.contentDOM.dispatchEvent(ev);'
        'return ev.defaultPrevented;'
    )
    screen.wait_for(lambda: 'Mod-s' in events)
    assert default_prevented_s is True, 'Mod-s should have called preventDefault'

    default_prevented_c = screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'const ev = new KeyboardEvent("keydown", {'
        f'key: "c", code: "KeyC", {_MOD_KEY_JS}, bubbles: true, cancelable: true}});'
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
        f'key: "s", code: "KeyS", {_MOD_KEY_JS}, bubbles: true, cancelable: true,'
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


def test_keybinding_invalid_modifier_raises():
    """An unrecognized modifier token raises ValueError at registration.

    Without this, a bad spec compiles into CM6's combined keymap and throws on the first keydown,
    which kills *every* binding (basicSetup undo/Tab and all valid user bindings) with only a console error.
    """
    from nicegui.elements.codemirror.keybindings import _validate_keybinding
    for good in ('Mod-s', 'F5', 'Mod-Shift-d', 'a', 'Ctrl-Alt-Delete', 'Cmd-Down', 'Mod--', '-',
                 'Ctrl-x Ctrl-s', 'Mod-k Mod-d'):  # incl. space-separated multi-stroke chords
        _validate_keybinding(good)  # valid descriptors must not raise
    for bad in ('Bogus-x', 'Ctr-s', 'Mod-Shift-Boop-d'):
        with pytest.raises(ValueError):
            _validate_keybinding(bad)


def test_keybinding_does_not_fire_while_disabled(screen: Screen):
    """Keybindings stop firing while the editor is disabled and resume once re-enabled."""
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello', keybindings={'Mod-s': lambda e: events.append(e.key)})

    screen.open('/')
    _wait_for_cm_mount(screen)

    dispatch = (
        f'const el = getElement({editor.id});'
        'el.editor.contentDOM.dispatchEvent(new KeyboardEvent("keydown", {'
        f'key: "s", code: "KeyS", {_MOD_KEY_JS}, bubbles: true, cancelable: true,'
        '}));'
    )
    content_editable = f'return getElement({editor.id}).editor.contentDOM.contentEditable;'

    screen.selenium.execute_script(dispatch)
    screen.wait_for(lambda: len(events) == 1)

    editor.disable()
    WebDriverWait(screen.selenium, 5).until(lambda d: d.execute_script(content_editable) == 'false')
    screen.selenium.execute_script(dispatch)  # must not fire while disabled

    editor.enable()
    WebDriverWait(screen.selenium, 5).until(lambda d: d.execute_script(content_editable) == 'true')
    screen.selenium.execute_script(dispatch)

    # WS delivery is FIFO: once the post-enable event arrives, any disabled-period event would have too.
    screen.wait_for(lambda: len(events) == 2)
    assert len(events) == 2, f'disabled editor should not have fired a keybinding, got {events}'


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
