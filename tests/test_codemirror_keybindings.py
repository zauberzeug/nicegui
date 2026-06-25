import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from nicegui import ui
from nicegui.testing import Screen

# CodeMirror resolves 'Mod' to Cmd on macOS and Ctrl elsewhere, so synthesized keydowns must use the
# matching modifier or the keybinding tests fail for Mac devs while passing on the Linux CI runner.
# Mirror CM6's own platform check as a computed property name (resolves to ctrlKey on Linux, metaKey on Mac).
_MOD_KEY_JS = '[/Mac/.test(navigator.platform) ? "metaKey" : "ctrlKey"]: true'


def _wait_for_cm_mount(screen: Screen) -> None:
    """Block until CM6 has inserted its contentDOM, proving the editor is ready for keydown dispatch."""
    WebDriverWait(screen.selenium, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.cm-content'))
    )


def test_keybinding_constructor(screen: Screen):
    """Bindings supplied via constructor fire on matching keystrokes and override basicSetup defaults."""
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(
            'hello',
            keymap={
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
    """Bindings added via map_key after mount fire correctly and win over basicSetup defaults.

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
    editor.map_key('Mod-z', lambda e: events.append(e.key))
    WebDriverWait(screen.selenium, 5).until(
        lambda d: d.execute_script(
            f'const el = getElement({editor.id});'
            'return (el.$props.keymap || []).some(b => b.key === "Mod-z");'
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
        editor = ui.codemirror('hello', keymap={'Mod-s': lambda: events.append('first')})
        editor.map_key('Mod-s', lambda: events.append('second'))

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
        editor = ui.codemirror('hello', keymap={'F2': lambda e: events.append({'key': e.key})})
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
        editor = ui.codemirror('hello', keymap={
            'Mod-s': lambda e: events.append(e.key),
            'Mod-c': ui.codemirror.KeyBinding(lambda e: events.append(e.key), prevent_default=False),
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
    """Per-OS overrides (mac/linux/win) surface in the keymap prop sent to JS.

    We can't trigger CM6's per-OS keybinding resolution from a single Linux test runner,
    but we can verify the prop payload carries the right fields so CM6 will use them on
    each platform.
    """
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello', keymap={
            'Alt-Down': ui.codemirror.KeyBinding(
                lambda: None, mac='Cmd-Down', linux='Ctrl-Down', win='Ctrl-Shift-Down',
            ),
            'F5': lambda: None,
        })

    screen.open('/')
    _wait_for_cm_mount(screen)
    bindings = screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'return el.$props.keymap;'
    )
    by_key = {b['key']: b for b in bindings}
    assert by_key['Alt-Down'].get('mac') == 'Cmd-Down', f'expected mac field, got {by_key["Alt-Down"]}'
    assert by_key['Alt-Down'].get('linux') == 'Ctrl-Down', f'expected linux field, got {by_key["Alt-Down"]}'
    assert by_key['Alt-Down'].get('win') == 'Ctrl-Shift-Down', f'expected win field, got {by_key["Alt-Down"]}'
    for field in ('mac', 'linux', 'win'):
        assert field not in by_key['F5'], f'F5 should have no {field} field, got {by_key["F5"]}'


def test_unmap_key(screen: Screen):
    """unmap_key removes a mapping so subsequent presses produce no event."""
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello', keymap={
            'Mod-s': lambda: events.append('save'),
            'F2': lambda e: events.append(f'control:{e.key}'),
        })
        editor.unmap_key('Mod-s')

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


@pytest.mark.parametrize('keybinding, error', [
    pytest.param('Ctr-s', 'Unrecognized modifier name', id='bad-modifier'),  # 'Ctr' is not a valid modifier
    pytest.param('Mod-a Mod-b', 'used both as a regular binding and as a multi-stroke prefix', id='prefix-conflict'),
])
def test_invalid_keybinding_is_reported(screen: Screen, keybinding: str, error: str):
    """A keybinding CodeMirror rejects at keymap-build time is reported to the server log, not silently swallowed.

    'Ctr-s' has an unrecognized modifier; 'Mod-a Mod-b' uses Mod-a as a chord prefix while basicSetup already
    binds Mod-a (select-all). Both make CodeMirror's keymap build throw, which the editor forces at registration
    and reports via logAndEmit instead of silently killing every keybinding on the first keypress.
    """
    @ui.page('/')
    def page():
        ui.codemirror('hello', keymap={keybinding: lambda: None})

    screen.allowed_js_errors.append(error)
    screen.open('/')
    _wait_for_cm_mount(screen)
    screen.wait_for(lambda: any(error in record.message for record in screen.caplog.records))
    screen.assert_py_logger('ERROR', re.compile(error))


def test_keybinding_does_not_fire_while_disabled(screen: Screen):
    """Keybindings stop firing while the editor is disabled and resume once re-enabled."""
    events: list[str] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello', keymap={'Mod-s': lambda e: events.append(e.key)})

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
