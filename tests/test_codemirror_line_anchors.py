from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


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
    editor.line_anchors = {'a1': 2, 'a2': 4}
    screen.wait_for(lambda: editor.line_anchors == {'a1': 2, 'a2': 4})


def test_line_anchors_replace_and_clear(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = {'x': 1, 'y': 2}
    screen.wait_for(lambda: editor.line_anchors == {'x': 1, 'y': 2})
    editor.line_anchors = {'z': 3}
    screen.wait_for(lambda: editor.line_anchors == {'z': 3})
    editor.line_anchors = {}
    screen.wait_for(lambda: editor.line_anchors == {})


def test_clear_after_typing_does_not_resurrect_anchors(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = {'mid': 3}
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 3)
    # The pending JS debounce timer plus the explicit clear must converge to an
    # empty mirror — a stale late-fire emit must not resurrect the cleared anchor.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    editor.line_anchors = {}
    screen.wait_for(lambda: editor.line_anchors == {})
    screen.wait(0.2)
    assert editor.line_anchors == {}


def test_anchor_remap_on_edit(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = {'mid': 3}
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 3)
    # Insert a new line at the very start; line 3 should remap to line 4.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 4)


def test_anchor_notifications_coalesce_during_typing(screen: Screen):
    """A burst of edits that keeps moving the anchors is reported once, not once per edit."""
    editor = None
    notifications: list[dict] = []

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello\nworld\n!')
        editor.on_anchor_change(lambda e: notifications.append(e.anchors))

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = {'a': 2, 'b': 3}
    screen.wait_for(lambda: editor.line_anchors == {'a': 2, 'b': 3})
    notifications.clear()
    # Dispatch 10 line insertions synchronously from JS so they all land within one debounce window,
    # regardless of Selenium IPC speed: the anchors move ten times but should be reported once.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'for (let i = 0; i < 10; i++) el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    screen.wait(0.2)
    assert notifications == [{'a': 12, 'b': 13}], \
        f'ten edits within one debounce window should be reported once, got {notifications}'


def test_no_notification_when_anchors_do_not_move(screen: Screen):
    """Editing elsewhere in the document must not notify about unchanged positions."""
    editor = None
    notifications: list[dict] = []

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('hello\nworld\n!')
        editor.on_anchor_change(lambda e: notifications.append(e.anchors))

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = {'a': 2, 'b': 3}
    screen.wait_for(lambda: editor.line_anchors == {'a': 2, 'b': 3})
    notifications.clear()
    # Appending to the last line leaves every anchor on the line it is already on.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'for (let i = 0; i < 5; i++)'
        '  el.editor.dispatch({changes: {from: el.editor.state.doc.length, insert: "y"}});'
    )
    screen.wait(0.2)
    assert notifications == [], f'edits that move no anchor should not notify, got {notifications}'


def test_anchor_positions_survive_unrelated_prop_update(screen: Screen):
    """An unrelated prop change must not snap remapped anchors back to their declared lines."""
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = {'mid': 3}
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 3)
    # Remap the anchor by inserting a line at the top: mid moves from line 3 to line 4.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 4)
    # Changing an unrelated prop re-broadcasts all props and re-fires the lineAnchors watcher;
    # the live position must survive instead of resetting to the declared line 3.
    editor.theme = 'oneDark'
    screen.wait_for_js(f'getElement({editor.id}).$props.theme', 'oneDark', timeout=5)
    screen.wait(0.2)
    assert editor.line_anchors == {'mid': 4}, \
        f'anchor positions should survive an unrelated prop update, got {editor.line_anchors}'


def test_reassign_same_declared_value_snaps_back(screen: Screen):
    """A deliberate reassignment must re-apply the declared lines even if the value is unchanged."""
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = {'mid': 3}
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 3)
    # Remap the anchor by inserting a line at the top: mid moves from line 3 to line 4.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 4)
    # Reassigning the identical declared dict is an intent signal (not detectable by value comparison):
    # it must not be preserved like an unrelated re-broadcast, but snap the anchor back to line 3.
    editor.line_anchors = {'mid': 3}
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 3)


def test_last_anchor_deletion_notifies(screen: Screen):
    """Deleting the only anchor (field size 1 -> 0) still notifies Python."""
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc')

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = {'only': 2}
    screen.wait_for(lambda: editor.line_anchors == {'only': 2})
    # Delete a range straddling the anchor's position so CodeMirror drops it (TrackDel).
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 1, to: 3}});'
    )
    screen.wait_for(lambda: editor.line_anchors == {})


def test_anchors_survive_client_side_remount(screen: Screen):
    """A remount without a server round-trip must restore the live positions, not the declared ones."""
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        with ui.tabs() as tabs:
            ui.tab('One')
            ui.tab('Two')
        with ui.tab_panels(tabs, value='One', keep_alive=False):
            with ui.tab_panel('One'):
                editor = ui.codemirror('a\nb\nc\nd\ne', line_anchors={'mid': 3})
            with ui.tab_panel('Two'):
                ui.label('Second tab')

    screen.open('/')
    _wait_for_editor(screen)
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 3)
    # Remap the anchor by inserting a line at the top: mid moves from line 3 to line 4.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    screen.wait_for(lambda: editor.line_anchors.get('mid') == 4)
    # Leaving the tab destroys the editor client-side; coming back builds a fresh one from the props.
    screen.click('Two')
    screen.should_contain('Second tab')
    screen.click('One')
    _wait_for_editor(screen)
    screen.wait(0.2)
    assert editor.line_anchors == {'mid': 4}, \
        f'anchors should survive a client-side remount, got {editor.line_anchors}'


def test_on_anchor_change_handler(screen: Screen):
    """on_anchor_change fires with the current positions on every change."""
    editor = None
    received: list[dict] = []

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('a\nb\nc\nd\ne', on_anchor_change=lambda e: received.append(e.anchors))

    screen.open('/')
    _wait_for_editor(screen)
    editor.line_anchors = {'mid': 3}
    screen.wait_for(lambda: bool(received) and received[-1] == {'mid': 3})
    # A remapping edit fires the handler again with the new line.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({changes: {from: 0, insert: "X\\n"}});'
    )
    screen.wait_for(lambda: received[-1] == {'mid': 4})
