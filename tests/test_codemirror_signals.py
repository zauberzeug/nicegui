import re

import pytest

from nicegui import ui
from nicegui.testing import Screen


def test_selection_change_event(screen: Screen):
    events: list[tuple[list[tuple[int, int]], int]] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(
            'Line 1\nLine 2\nLine 3\n😎abc',
            on_selection_change=lambda e: events.append(([(r.anchor, r.head) for r in e.ranges], e.main_index)),
        )

    def select(js: str) -> None:
        screen.selenium.execute_script(f'const view = getElement({editor.id}).editor; {js}')

    screen.open('/')
    screen.should_contain('Line 2')
    select('view.dispatch({selection: {anchor: view.state.doc.line(2).from + 3}});')
    screen.wait_for(lambda: events[-1:] == [([(10, 10)], 0)])

    # A backward selection keeps the anchor where it started and the head at the cursor.
    select('view.dispatch({selection: {anchor: view.state.doc.line(3).from + 2, head: 0}});')
    screen.wait_for(lambda: events[-1:] == [([(16, 0)], 0)])

    # With several cursors, every range is reported along with the main one.
    select('const S = view.state.selection.constructor;'
           'view.dispatch({selection: S.create([S.cursor(1), S.range(3, 5)], 1)});')
    screen.wait_for(lambda: events[-1:] == [([(1, 1), (3, 5)], 1)])

    # Positions are str indices: the emoji is one character in Python but two UTF-16 code units in the browser.
    select('view.dispatch({selection: {anchor: view.state.doc.line(4).from + 2, head: view.state.doc.length}});')
    screen.wait_for(lambda: events[-1:] == [([(22, 25)], 0)])
    assert editor.value[22:25] == 'abc'


def test_set_value_emits_only_when_the_selection_actually_moves(screen: Screen):
    """A server-driven value change emits only if it moved the selection.

    An edit that leaves the selection alone would otherwise reach the host as an echo of the selection it already knows.
    But `set_value` replaces only the changed region, so CodeMirror maps the selection through it:
    an edit before the cursor does move it, and a host told nothing would go on pointing at the wrong place.
    """
    events: list[int] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('ab\ncd\nef', on_selection_change=lambda e: events.append(e.main.head))

    screen.open('/')
    screen.should_contain('cd')
    # The cursor is at 0, after which this edit happens; nothing has been sent yet that a dedupe could compare with.
    editor.set_value('ab\ncd\nef changed')
    screen.should_contain('ef changed')
    screen.selenium.execute_script(f'getElement({editor.id}).editor.dispatch({{selection: {{anchor: 3}}}});')
    screen.wait_for(lambda: events == [3])

    editor.set_value('NEW\nab\ncd\nef changed')
    screen.wait_for(lambda: events == [3, 7])

    # The cursor keeps its place in the browser's UTF-16 code units, but moves one str index to the left.
    editor.set_value('NEW\n😎\ncd\nef changed')
    screen.wait_for(lambda: events == [3, 7, 6])
    assert editor.value[6:8] == 'cd'


def test_focus_change_event(screen: Screen):
    events: list[bool] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('Line 1\nLine 2\nLine 3', on_focus_change=lambda e: events.append(e.focused))

    screen.open('/')
    screen.should_contain('Line 2')
    # Focus via JS to avoid Selenium focus-stealing flakiness.
    screen.selenium.execute_script(f'getElement({editor.id}).editor.focus();')
    screen.wait_for(lambda: events == [True])
    screen.selenium.execute_script(f'getElement({editor.id}).editor.contentDOM.blur();')
    screen.wait_for(lambda: events == [True, False])


@pytest.mark.parametrize('transform', ['none', 'scale(0.5)'])
def test_viewport_change_event_follows_reveal_line(screen: Screen, transform: str):
    events: list[tuple[int, int]] = []
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(
            '\n'.join(f'Line {i}' for i in range(1, 201)),
            on_viewport_change=lambda e: events.append((e.from_line, e.to_line)),
        ).style(f'transform: {transform}')

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
    screen.wait_for(lambda: any(height >= 200 for _, height, _ in events))

    # `content_height` comes off CodeMirror in scaled pixels while the width and
    # height beside it are layout pixels. A CSS transform changes neither the
    # document nor the space it is laid out in, so all three have to sit still.
    baseline = next(c for _, h, c in events if h >= 200)
    screen.selenium.execute_script(
        f'const el = getElement({editor.id});'
        'el.$el.style.transform = "scale(0.5)";'
        'el.$el.style.height = "300px";'
    )
    screen.wait_for(lambda: any(height == 300 for _, height, _ in events))
    assert next(c for _, h, c in events if h == 300) == baseline
