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


@doc.demo('Cursor Tracking, Save Shortcut, and Reveal Line', '''
    ``on_cursor_line`` reports the 1-indexed line number whenever the cursor moves to a different line.
    ``on_save`` fires when the user presses Ctrl/Cmd+S inside the editor and suppresses the browser's default save dialog.
    ``reveal_line`` scrolls a given line into view.
''')
def cursor_save_reveal_demo() -> None:
    status = ui.label('Cursor: line 1')
    editor = ui.codemirror(
        '\n'.join(f'Line {i}' for i in range(1, 31)),
        on_cursor_line=lambda e: status.set_text(f'Cursor: line {e.line}'),
        on_save=lambda _: ui.notify('Saved!'),
    ).classes('h-32')
    ui.button('Reveal line 20', on_click=lambda: editor.reveal_line(20))


doc.reference(ui.codemirror)
