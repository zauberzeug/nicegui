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

    Side-panel ``info`` content renders as plain text by default; pass
    ``completion_info_html=True`` to the constructor to render ``info`` as sanitized HTML
    via NiceGUI's ``setHTML`` polyfill — useful for code samples, links, or formatted notes.
''')
def custom_completions_demo() -> None:
    editor = ui.codemirror('', language='Python', completion_info_html=True, completions=[
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


@doc.demo('Custom Keybindings', '''
    Map keystrokes to Python callbacks via the `keymap` constructor parameter or the `map_key` method.
    Keys follow CodeMirror's [keymap syntax](https://codemirror.net/docs/ref/#view.KeyBinding) —
    use "Mod" for Cmd on macOS and Ctrl elsewhere.

    By default, keybindings prevent the browser default action so they can override shortcuts like "Mod-s".
    Wrap a callback with `ui.codemirror.KeyBinding(...)` to override that (`prevent_default=False`)
    or to provide per-platform shortcut overrides (`mac=`, `linux=`, `win=`).

    Use `unmap_key(key)` to remove a mapping at runtime.

    *Added in version 3.14.0*
''')
def keymap_demo() -> None:
    editor = ui.codemirror(
        keymap={
            'a': lambda: ui.notify('Pressed a'),
            'Ctrl-c': lambda: ui.notify('Pressed Ctrl-c'),
            'Mod-r': lambda: ui.notify('Pressed Mod-r'),
            'Mod-s': ui.codemirror.KeyBinding(
                lambda: ui.notify('Pressed Mod-s (no prevent_default)'),
                prevent_default=False,
            ),
            'Mod-x Mod-y': lambda: ui.notify('Pressed Mod-x then Mod-y'),
        },
    ).classes('h-32')
    ui.button('Map F5', on_click=lambda: editor.map_key('F5', lambda: ui.notify('Pressed F5')))
    ui.button('Unmap F5', on_click=lambda: editor.unmap_key('F5'))


@doc.demo('Hover tooltips on lines', '''
    `line_tooltips` maps 1-indexed line numbers to hover content.

    *Added in version 3.13.0*
''')
def line_tooltips_demo() -> None:
    editor = ui.codemirror(
        'def add(a, b):\n'
        '    """Sum two numbers."""\n'
        '    return a + b\n',
    ).classes('h-40')
    editor.line_tooltips[1] = 'symbol: add, arity: 2'
    editor.line_tooltips[3] = 'returns the sum of a and b'


@doc.demo('HTML rendering for tooltips', '''
    Pass `line_tooltip_html=True` to render tooltip content as HTML,
    sanitized via NiceGUI's DOMPurify-backed `setHTML` polyfill.

    *Added in version 3.13.0*
''')
def line_tooltip_html_demo() -> None:
    editor = ui.codemirror(
        'def add(a, b):\n'
        '    return a + b\n',
        line_tooltip_html=True,
    ).classes('h-32')
    editor.line_tooltips[2] = '<b>returns</b> the sum of <code>a</code> and <code>b</code>'


doc.reference(ui.codemirror)
