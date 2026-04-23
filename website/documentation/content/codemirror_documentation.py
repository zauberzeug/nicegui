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


@doc.demo('Custom Completions', '''
    ``custom_completions`` (and the ``set_custom_completions`` setter) installs an autocomplete source.
    Each entry is a dict with at least ``label``;
    ``apply``, ``detail``, ``info``, and ``type`` (``'function'``, ``'variable'``, ``'class'``, ``'keyword'``, etc.) are optional.
''')
def custom_completions_demo() -> None:
    ui.codemirror('', language='Python', custom_completions=[
        {'label': 'np.array', 'apply': 'np.array(', 'detail': 'numpy.array(...)', 'type': 'function'},
        {'label': 'np.zeros', 'apply': 'np.zeros(', 'detail': 'numpy.zeros(shape, dtype=...)', 'type': 'function'},
        {'label': 'np.pi', 'detail': 'numpy constant', 'type': 'variable'},
    ]).classes('h-32')


doc.reference(ui.codemirror)
