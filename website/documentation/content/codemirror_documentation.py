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


@doc.demo('Autocomplete', '''
    Pass ``completions`` to surface your own entries in the autocomplete dropdown.
    Each item is a dict; only ``label`` is required.
    ``apply`` controls the inserted text, ``detail``/``info`` add helper text,
    ``type`` picks an icon, ``boost`` biases sort order (-99..99),
    ``display_label`` overrides the visible text, ``section`` groups entries under a heading,
    ``commit_characters`` are extra accept-keys, and ``class_name`` adds a CSS class to that entry.

    Set ``snippet=True`` and use ``${1:foo}`` markers in ``apply`` for templated insertions —
    Tab cycles between fields. By default your entries merge with the active language pack's
    completions; pass ``replace_language_completions=True`` to suppress them. Set
    ``complete_words_in_document=True`` to also surface identifiers already typed elsewhere.
    Call ``editor.trigger_completion()`` to open the popup programmatically.

    The side-panel ``info`` content renders via NiceGUI's global ``setHTML`` polyfill, so plain
    text and sanitized HTML both work — useful for code samples, links, or formatted notes.
''')
def custom_completions_demo() -> None:
    editor = ui.codemirror('', language='Python', completions=[
        {'label': 'np.array', 'apply': 'np.array(', 'detail': 'numpy.array(...)',
         'info': 'Build an N-D array. <code>np.array([1, 2, 3])</code> &rarr; <b>1-D</b>.',
         'type': 'function', 'section': 'numpy', 'commit_characters': ['(']},
        {'label': 'np.zeros', 'apply': 'np.zeros(', 'detail': 'numpy.zeros(shape, dtype=...)',
         'type': 'function', 'section': 'numpy', 'boost': 99},
        {'label': 'np.pi', 'display_label': 'np.pi (constant)',
         'detail': 'numpy constant', 'type': 'variable', 'section': 'numpy'},
        {'label': 'forloop', 'display_label': 'for', 'snippet': True,
         'apply': 'for ${1:item} in ${2:iterable}:\n    ${3:pass}',
         'type': 'keyword', 'detail': 'for-loop snippet'},
        {'label': 'old_func', 'class_name': 'cm-deprecated',
         'detail': 'use new_func instead'},
        {'label': 'TODO'},
    ], tooltip_class='cm-popup-wide').classes('h-40')

    ui.add_css('.cm-deprecated { text-decoration: line-through; opacity: 0.6; }'
               '.cm-popup-wide { min-width: 320px; }')

    ui.button('Suggest', on_click=editor.trigger_completion)


doc.reference(ui.codemirror)
