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


@doc.demo('Linting Diagnostics', '''
    ``set_diagnostics`` renders inline error/warning marks with hover tooltips.
    Each diagnostic targets a 1-indexed line and carries a message; ``severity`` and ``source`` are optional.
    ``clear_diagnostics`` removes all of them.
''')
def diagnostics_demo() -> None:
    editor = ui.codemirror('def add(a, b):\n    return a + c\n', language='Python').classes('h-32')
    ui.button('Lint', on_click=lambda: editor.set_diagnostics([
        {'line': 2, 'message': "undefined name 'c'", 'severity': 'error', 'source': 'pyflakes'},
    ]))
    ui.button('Clear', on_click=editor.clear_diagnostics)


doc.reference(ui.codemirror)
