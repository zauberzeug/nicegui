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
    Anchors give you a stable handle to a specific line that survives edits.
    Use them to detect "did anything that matters change?" — pure whitespace edits leave
    anchor positions intact, so you can skip expensive re-analysis.
''')
def line_anchors_demo() -> None:
    code = (
        'def add(a, b):\n'
        '    return a + b\n'
        '\n'
        'def mul(a, b):\n'
        '    return a * b\n'
    )
    editor = ui.codemirror(code, language='Python').classes('h-40')
    editor.set_line_anchors([{'id': 'add', 'line': 1}, {'id': 'mul', 'line': 4}])

    status = ui.label('Code structure unchanged — skip re-analysis').classes('text-positive')
    initial = {'add': 1, 'mul': 4}

    def check(_) -> None:
        positions = editor.line_anchor_positions.get('default', {})
        if positions == initial:
            status.set_text('Code structure unchanged — skip re-analysis')
            status.classes(replace='text-positive')
        else:
            status.set_text(f'Anchors moved: {positions} — re-analyze')
            status.classes(replace='text-negative')

    editor.on('anchor-positions', check)


doc.reference(ui.codemirror)
