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


@doc.demo('Decorations and line flash', '''
    `set_decorations` lets you add styled mark or line decorations on top of any text.
    The host application supplies its own CSS for whatever class names it passes.
    `highlight_lines` is a convenience for transient line emphasis: it applies a class to
    the given lines for `duration_ms` and then clears it on the client without a server
    round-trip — useful for CSS keyframe animations that pulse a "look here" effect.
''')
def decorations_demo() -> None:
    ui.add_head_html('''
        <style>
            .my-error  { background-color: rgba(255, 0,   0, 0.2); }
            .my-flash  { animation: my-flash 1s ease-out forwards; }
            @keyframes my-flash {
                0%   { background-color: rgba(255, 200, 0, 0.5); }
                100% { background-color: transparent; }
            }
        </style>
    ''')
    editor = ui.codemirror('alpha\nbeta\ngamma\ndelta\nepsilon').classes('h-32')
    ui.button('Mark line 2 red', on_click=lambda: editor.set_decorations(
        [{'kind': 'line', 'line': 2, 'class': 'my-error'}],
    ))
    ui.button('Flash lines 4 and 5', on_click=lambda: editor.highlight_lines(
        [4, 5], css_class='my-flash', duration_ms=1000,
    ))
    ui.button('Clear', on_click=editor.clear_decorations)


doc.reference(ui.codemirror)
