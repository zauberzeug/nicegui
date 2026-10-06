import re

import pytest

from nicegui import ui
from nicegui.testing import Screen


def test_selection_change_event(screen: Screen):
    events: list[tuple[int, int, int, int, bool]] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(
            'Line 1\nLine 2\nLine 3\n😎abc',
            on_selection_change=lambda e: events.append((e.line, e.column, e.from_line, e.to_line, e.empty)),
        )

    screen.open('/')
    screen.should_contain('Line 2')
    # Move the cursor to line 2, column 4 (3 chars past line.from) via a CM6 selection transaction.
    # This bypasses focus/keystroke timing fragility in Selenium.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({selection: {anchor: el.editor.state.doc.line(2).from + 3}});'
    )
    screen.wait_for(lambda: (2, 4, 2, 2, True) in events)
    # A ranged selection from line 1 into line 3 spans from_line=1..to_line=3
    # regardless of head direction (head at the anchor end here).
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({selection: {anchor: el.editor.state.doc.line(3).from + 2, head: 0}});'
    )
    screen.wait_for(lambda: (1, 1, 1, 3, False) in events)
    # `column` counts code points, so it indexes the Python string the same way:
    # the cursor after "😎abc" is column 5, not the 6 that UTF-16 code units would report.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({selection: {anchor: el.editor.state.doc.line(4).to}});'
    )
    screen.wait_for(lambda: (4, 5, 4, 4, True) in events)


def test_set_value_emits_only_when_the_cursor_actually_moves(screen: Screen):
    """A server-driven value change emits only if it moved the cursor.

    An edit that leaves the cursor alone would otherwise reach the host as an
    echo indistinguishable from a real cursor move. But `set_value` replaces
    only the changed region, so CodeMirror remaps the selection through it: an
    edit above the cursor does move it, and a host told nothing would go on
    pointing at the wrong line.
    """
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
    before = len(events)
    editor.set_value('Line 1\nLine 2 changed\nLine 3')
    screen.should_contain('Line 2 changed')
    # A real cursor move afterwards must still emit; waiting for it proves the
    # assertion below gave any echo from set_value time to arrive.
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.editor.dispatch({selection: {anchor: el.editor.state.doc.line(3).from}});'
    )
    screen.wait_for(lambda: (3, 1) in events)
    assert len(events) == before + 1

    # Inserting a line above the cursor remaps it from line 3 to line 4.
    editor.set_value('NEW\nLine 1\nLine 2 changed\nLine 3')
    screen.should_contain('NEW')
    screen.wait_for(lambda: (4, 1) in events)


def test_focus_change_event(screen: Screen):
    """Focus changes are reported, and ahead of the selection that comes with them.

    A host ignoring selection events while the editor is unfocused (programmatic echoes) relies on both:
    the focus event has to arrive first, and the first selection after it has to be emitted
    even when it matches the last one sent.
    """
    events: list[bool | tuple[int, int]] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(
            'Line 1\nLine 2\nLine 3',
            on_focus_change=lambda e: events.append(e.focused),
            on_selection_change=lambda e: events.append((e.line, e.column)),
        )

    screen.open('/')
    screen.should_contain('Line 2')
    # Focus and select via JS to avoid Selenium focus-stealing flakiness;
    # like a click into the editor, this puts both into a single editor update.
    focus_and_select = (
        f'const el = getElement({editor.id}); el.editor.focus();'
        'el.editor.dispatch({selection: {anchor: el.editor.state.doc.line(2).from}});'
    )
    screen.selenium.execute_script(focus_and_select)
    screen.wait_for(lambda: len(events) == 2)
    assert events == [True, (2, 1)]

    screen.selenium.execute_script(f'getElement({editor.id}).editor.contentDOM.blur();')
    screen.wait_for(lambda: len(events) == 3)
    screen.selenium.execute_script(focus_and_select)
    screen.wait_for(lambda: len(events) == 5)
    assert events == [True, (2, 1), False, True, (2, 1)]


def test_viewport_change_event_follows_reveal_line(screen: Screen):
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
    screen.wait_for(lambda: len(events) > 0)
    from_line, to_line = events[-1]
    assert from_line == 1 and to_line < 30, 'only the lines on screen should be reported, not the whole document'

    editor.reveal_line(150)
    screen.wait_for(lambda: events[-1][0] < 150 < events[-1][1])
    from_line, to_line = events[-1]
    assert to_line - from_line < 30, 'only the lines on screen should be reported, not the whole document'

    editor.reveal_line(500)
    screen.wait_for(lambda: any('reveal_line' in record.message for record in screen.caplog.records))
    screen.assert_py_logger('WARNING', re.compile(r'reveal_line: line 500 out of range \[1, 200\]'))


@pytest.mark.parametrize('layout', ['scrolling editor', 'scrolling page', 'scroll area'])
def test_reveal_line_brings_the_line_into_sight(screen: Screen, layout: str):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        text = '\n'.join(f'Line {i}' for i in range(1, 201))
        if layout == 'scrolling editor':
            editor = ui.codemirror(text)
        elif layout == 'scrolling page':
            editor = ui.codemirror(text).classes('h-auto')
        else:
            with ui.scroll_area().classes('h-64'):
                editor = ui.codemirror(text).classes('h-[600px]')

    screen.open('/')
    screen.should_contain('Line 1')
    editor.reveal_line(150)
    # Visible means not clipped by the editor, a surrounding scroll area or the window,
    # which is what the element at the line's on-screen position tells.
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const view = getElement({editor.id}).editor;'
        'const block = view.lineBlockAt(view.state.doc.line(150).from);'
        'const y = view.documentTop + block.top + block.height / 2;'
        'const hit = document.elementFromPoint(view.contentDOM.getBoundingClientRect().left + 8, y);'
        'return hit?.closest(".cm-line")?.textContent;'
    ) == 'Line 150')


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

    # `content_height` comes off CodeMirror in scaled pixels while the width and
    # height beside it are layout pixels. A CSS transform changes neither the
    # document nor the space it is laid out in, so all three have to sit still.
    baseline = next(c for _, h, c in events if h >= 200)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.$el.style.transform = "scale(0.5)";'
        'el.$el.style.height = "300px";'
        'el.editor.requestMeasure();'
    )
    screen.wait_for(lambda: any(height == 300 for _, height, _ in events))
    assert next(c for _, h, c in events if h == 300) == baseline
