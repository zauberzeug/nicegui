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
    Each diagnostic targets a 1-indexed line and carries a message; ``severity``, ``source``,
    and the column range (``column`` and ``end_column``, 1-indexed; ``end_column`` is exclusive) are optional.
    ``clear_diagnostics`` removes all of them. ``open_lint_panel``, ``close_lint_panel``, and
    ``toggle_lint_panel`` show or hide CodeMirror's built-in panel listing the diagnostics, and
    ``get_diagnostic_count`` returns the count by severity.
''')
def diagnostics_demo() -> None:
    editor = ui.codemirror('def add(a, b):\n    return a + c\n', language='Python').classes('h-32')
    count_label = ui.label()

    async def lint() -> None:
        editor.set_diagnostics([
            {'line': 2, 'message': "undefined name 'c'", 'severity': 'error',
             'source': 'pyflakes', 'column': 16, 'end_column': 17},
        ])
        count_label.text = str(await editor.get_diagnostic_count())

    ui.button('Lint', on_click=lint)
    ui.button('Clear', on_click=editor.clear_diagnostics)
    ui.button('Toggle Panel', on_click=editor.toggle_lint_panel)


doc.reference(ui.codemirror)
