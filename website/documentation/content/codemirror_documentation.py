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


@doc.demo('Custom Keybindings', '''
    Map keystrokes to Python callbacks via the ``keybindings`` constructor parameter or the ``on_keybinding`` method.
    Keys follow CodeMirror's [keymap syntax](https://codemirror.net/docs/ref/#view.KeyBinding) —
    use ``Mod`` for Cmd on macOS and Ctrl elsewhere.

    By default, bindings prevent the browser default action so they can override shortcuts like ``Mod-s``.
    Wrap a callback with ``ui.codemirror.binding(...)`` to override that (``prevent_default=False``)
    or to provide per-platform shortcut overrides (``mac=``, ``linux=``, ``win=``).

    Use ``remove_keybinding(key)`` to unbind at runtime.
''')
def keybindings_demo() -> None:
    editor = ui.codemirror(
        keybindings={
            'a': lambda: ui.notify('Pressed a'),
            'Ctrl-c': lambda: ui.notify('Pressed Ctrl-c'),
            'Mod-r': lambda: ui.notify('Pressed Mod-r'),
            'Mod-s': ui.codemirror.binding(
                lambda: ui.notify('Pressed Mod-s (no prevent_default)'),
                prevent_default=False,
            ),
            'Mod-x Mod-y': lambda: ui.notify('Pressed Mod-x then Mod-y'),
        },
    ).classes('h-32')
    ui.button('Bind F5', on_click=lambda: editor.on_keybinding('F5', lambda: ui.notify('Pressed F5')))
    ui.button('Unbind F5', on_click=lambda: editor.remove_keybinding('F5'))


@doc.demo('Hover tooltips on lines', '''
    `line_tooltips` maps 1-indexed line numbers to hover content.

    *Added in NiceGUI 3.13.0*
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

    *Added in NiceGUI 3.13.0*
''')
def line_tooltip_html_demo() -> None:
    editor = ui.codemirror(
        'def add(a, b):\n'
        '    return a + b\n',
        line_tooltip_html=True,
    ).classes('h-32')
    editor.line_tooltips[2] = '<b>returns</b> the sum of <code>a</code> and <code>b</code>'


doc.reference(ui.codemirror)
