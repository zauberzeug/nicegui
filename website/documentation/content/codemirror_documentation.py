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


@doc.demo('Editor Signals and Reveal Line', '''
    ``on_selection_change`` reports the 1-indexed line and column whenever the cursor moves.
    ``on_viewport_change`` reports the visible line range — useful for confirming that
    ``reveal_line`` actually scrolled the requested line into view.
    Other signal hooks include ``on_focus_change`` and ``on_geometry_change``.
    Per-signal debounce can be tuned via ``ui.codemirror.handler(callback, debounce_ms=...)``.
''')
def signals_and_reveal_demo() -> None:
    cursor_status = ui.label('Cursor: line 1, col 1')
    viewport_status = ui.label('Viewport: ?')
    editor = ui.codemirror(
        '\n'.join(f'Line {i}' for i in range(1, 51)),
        on_selection_change=lambda e: cursor_status.set_text(f'Cursor: line {e.line}, col {e.column}'),
        on_viewport_change=lambda e: viewport_status.set_text(f'Viewport: lines {e.from_line}–{e.to_line}'),
    ).classes('h-32')
    ui.button('Reveal line 40', on_click=lambda: editor.reveal_line(40))


doc.reference(ui.codemirror)
