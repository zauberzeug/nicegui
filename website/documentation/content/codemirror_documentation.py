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
    Each entry is a dict; only ``label`` is required.
    ``apply`` controls the inserted text, ``detail``/``info`` add helper text,
    ``type`` picks an icon (one of ``'class'``, ``'constant'``, ``'enum'``, ``'function'``, ``'interface'``,
    ``'keyword'``, ``'method'``, ``'namespace'``, ``'property'``, ``'text'``, ``'type'``, ``'variable'``),
    ``boost`` biases sort order (higher floats to the top, range -99 to 99),
    ``displayLabel`` overrides the visible text while ``label`` is still used for matching,
    ``section`` groups entries under a heading, and ``commitCharacters`` are extra characters
    that accept the completion when typed.
''')
def custom_completions_demo() -> None:
    ui.codemirror('', language='Python', custom_completions=[
        {'label': 'np.array', 'apply': 'np.array(', 'detail': 'numpy.array(...)',
         'type': 'function', 'section': 'numpy', 'commitCharacters': ['(']},
        {'label': 'np.zeros', 'apply': 'np.zeros(', 'detail': 'numpy.zeros(shape, dtype=...)',
         'type': 'function', 'section': 'numpy', 'boost': 99},
        {'label': 'np.pi', 'displayLabel': 'np.pi (constant)',
         'detail': 'numpy constant', 'type': 'variable', 'section': 'numpy'},
        {'label': 'TODO'},  # no type → no icon, no section → ungrouped
    ]).classes('h-32')


doc.reference(ui.codemirror)
