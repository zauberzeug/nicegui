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


@doc.demo('Decorations', '''
    `set_decorations` adds styled overlays on top of the editor's text without modifying the
    document. There are four kinds:

    - **mark** — style a character range
    - **line** — style an entire line
    - **replace** — hide a range (no `text`) or replace it visually with text
    - **widget** — insert a text annotation at a position

    The host application supplies its own CSS for whatever class names it passes.
    Widget and replace `text` values render via NiceGUI's global `setHTML` polyfill,
    so plain text and sanitized HTML both work.
''')
def decorations_demo() -> None:
    ui.add_head_html('''
        <style>
            .my-error  { background-color: rgba(255, 0, 0, 0.2); }
            .my-fold   { color: #888; font-style: italic; padding: 0 4px; }
            .my-hint   { color: #888; font-size: 0.8em; padding: 0 4px; }
        </style>
    ''')
    editor = ui.codemirror('alpha\nbeta\ngamma\ndelta\nepsilon').classes('h-32')
    with ui.row():
        ui.button('Mark range', on_click=lambda: editor.set_decorations(
            [{'kind': 'mark', 'from': 6, 'to': 10, 'class': 'my-error'}],
        ))
        ui.button('Highlight line', on_click=lambda: editor.set_decorations(
            [{'kind': 'line', 'line': 3, 'class': 'my-error'}],
        ))
        ui.button('Fold lines', on_click=lambda: editor.set_decorations(
            [{'kind': 'replace', 'from': 6, 'to': 22,
              'text': '{ ... 3 lines ... }', 'class': 'my-fold', 'block': True}],
        ))
        ui.button('Annotate (HTML)', on_click=lambda: editor.set_decorations(
            [{'kind': 'widget', 'position': 5,
              'text': '<b style="color: #c00">⚠ first</b>'}],
        ))
        ui.button('Clear', on_click=editor.clear_decorations)


doc.reference(ui.codemirror)
