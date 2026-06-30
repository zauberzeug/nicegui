from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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
    editor.line_anchors = {'a': 1, 'b': 3}
    screen.wait_for(lambda: editor.line_anchors == {'a': 1, 'b': 3})
    emissions.clear()
    # Dispatch 10 doc changes synchronously from JS so they all land within the 50ms debounce
    # window, regardless of Selenium IPC speed. With coalescing we expect a single emission.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'for (let i = 0; i < 10; i++) el.editor.dispatch({changes: {from: 0, insert: "x"}});'
    )
    screen.wait(0.2)
    assert len(emissions) == 1, f'expected one coalesced emission for 10 synchronous edits, got {len(emissions)}'


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
    # Changing an unrelated prop re-broadcasts all props and re-fires the deep lineAnchors watcher;
    # the live position must survive instead of resetting to the declared line 3.
    editor.theme = 'oneDark'
    WebDriverWait(screen.selenium, 5).until(
        lambda d: d.execute_script(f'return getElement({editor.id}).$props.theme;') == 'oneDark'
    )
    screen.wait(0.2)
    assert editor.line_anchors == {'mid': 4}, \
        f'unrelated prop update reset anchors, got {editor.line_anchors}'


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
