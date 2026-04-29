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


@doc.demo('Hover tooltips on lines', '''
    `set_line_tooltips` attaches hover content to specific lines.
    Values render via NiceGUI's global DOMPurify-backed `setHTML` polyfill,
    so plain text and sanitized HTML both work — `<script>` tags and other unsafe markup are stripped.
''')
def line_tooltips_demo() -> None:
    editor = ui.codemirror(
        'def add(a, b):\n'
        '    """Sum two numbers."""\n'
        '    return a + b\n',
    ).classes('h-40')
    editor.set_line_tooltips({
        1: 'symbol: add, arity: 2',
        3: '<b>returns</b> the sum of <code>a</code> and <code>b</code>',
    })


doc.reference(ui.codemirror)
