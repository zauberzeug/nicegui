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
        with ui.tabs() as tabs:
            ui.tab('One')
            ui.tab('Two')
        with ui.tab_panels(tabs, value='One', keep_alive=False):
            with ui.tab_panel('One'):
                editor = ui.codemirror('ab\ncd', on_selection_change=lambda e: events.append(
                    ([(r.anchor, r.head) for r in e.ranges], e.main_index)))
            with ui.tab_panel('Two'):
                ui.label('Second tab')

    def run(js: str) -> None:
        screen.selenium.execute_script(f'const view = getElement({editor.id}).editor; {js}')

    def cursor_before_cd():
        i = editor.value.index('cd')
        return ([(i, i)], 0)

    screen.open('/')
    screen.should_contain('cd')
    # An edit after the cursor leaves it in place, so it is not reported, even before anything was sent.
    editor.set_value('ab\ncd changed')
    screen.should_contain('cd changed')
    run('view.dispatch({selection: {anchor: 3}});')
    screen.wait_for(lambda: events == [cursor_before_cd()])

    # An edit before the cursor moves it.
    editor.set_value('NEW\nab\ncd changed')
    screen.wait_for(lambda: len(events) == 2 and events[-1] == cursor_before_cd())

    # Positions are str indices: the emoji takes the two UTF-16 code units of "ab", but only one str index.
    editor.set_value('NEW\n😎\ncd changed')
    screen.wait_for(lambda: len(events) == 3 and events[-1] == cursor_before_cd())

    # A backward selection keeps the anchor where it started and the head at the cursor.
    run('view.dispatch({selection: {anchor: view.state.doc.length, head: 0}});')
    screen.wait_for(lambda: events[-1] == ([(len(editor.value), 0)], 0))

    # With several cursors, every range is reported along with the index of the main one.
    run('const S = view.state.selection.constructor, cd = view.state.doc.toString().indexOf("cd");'
        'view.dispatch({selection: S.create([S.cursor(1), S.range(cd, cd + 2)], 1)});')
    screen.wait_for(lambda: events[-1] == ([(1, 1), (editor.value.index('cd'), editor.value.index('cd') + 2)], 1))

    # Leaving the tab destroys the editor client-side; the one built on return has its cursor at the start
    # and has sent nothing yet, so selecting there is reported, replacing the selection from before.
    screen.click('Two')
    screen.should_contain('Second tab')
    screen.click('One')
    screen.should_contain('cd changed')
    run('view.dispatch({selection: {anchor: 0}});')
    screen.wait_for(lambda: events[-1] == ([(0, 0)], 0))


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
