from nicegui import ui

from . import doc


@doc.demo(ui.codemirror)
def main_demo() -> None:
    editor = ui.codemirror('print("Edit me!")', language='Python').classes('h-32')
    ui.select(editor.supported_languages, label='Language', clearable=True) \
        .classes('w-32').bind_value(editor, 'language')
    ui.select(editor.supported_themes, label='Theme') \
        .classes('w-32').bind_value(editor, 'theme')
    ui.checkbox('Wrap Lines', value=editor.line_wrapping,
                on_change=lambda e: editor.set_line_wrapping(e.value))


@doc.demo('Preserving Cursor Position', '''
    ``set_value`` applies only the modified region, so cursor positions and selections outside the change are preserved.
    Try editing the code below while the first line updates automatically.
''')
def preserve_cursor_demo() -> None:
    from datetime import datetime

    editor = ui.codemirror(f'# {datetime.now():%H:%M:%S}\n', language='Python')
    ui.timer(1, lambda: editor.set_value(
        f'# {datetime.now():%H:%M:%S}\n' + editor.value.split('\n', 1)[-1]
    ))


@doc.demo('Line Anchors', '''
    ``set_line_anchors`` pins caller-chosen IDs to specific lines.
    CodeMirror remaps the underlying positions through edits, and ``line_anchor_positions``
    mirrors the current line for each anchor on the Python side.
    Use this to track stable references to "where the user put a target" without storing line numbers
    that go stale as the document changes.
''')
def line_anchors_demo() -> None:
    editor = ui.codemirror('hello\nworld\nthird\nfourth').classes('h-32')
    label = ui.label()
    editor.set_line_anchors([{'id': 'a', 'line': 2}, {'id': 'b', 'line': 4}])

    def refresh():
        label.set_text(str(editor.line_anchor_positions))
    refresh()
    ui.button('Refresh', on_click=refresh)


doc.reference(ui.codemirror)
