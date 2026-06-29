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
    Line anchors give you a more stable reference to specific lines than line numbers.
    The browser tracks each anchor's position through every change — insertions, deletions, reformatting
    — and reading ``line_anchors`` back returns the current line on the Python side.
    The example below anchors the first line and rewrites it in place when you click "Update argument":
    edit the code freely (add blank lines above, indent, reorder) and the anchor still points at the right line.

    *Added in NiceGUI 3.14.0*
''')
def line_anchors_demo() -> None:
    editor = ui.codemirror('answer: 42', line_anchors={'answer': 1}) \
        .on_anchor_change(lambda e: ui.notify(e.anchors)) \
        .classes('h-40')

    def increment() -> None:
        lines = editor.value.split('\n')
        if (line_no := editor.line_anchors.get('answer')) and line_no <= len(lines):
            answer = int(lines[line_no - 1].split()[-1])
            lines[line_no - 1] = f'answer: {answer + 1}'
            editor.value = '\n'.join(lines)

    ui.button('Increment', on_click=increment)


@doc.demo('Custom Keybindings', '''
    Map keystrokes to Python callbacks via the `keymap` constructor parameter or the `map_key` method.
    Keys follow CodeMirror's [keymap syntax](https://codemirror.net/docs/ref/#view.KeyBinding) —
    use "Mod" for Cmd on macOS and Ctrl elsewhere.

    By default, keybindings prevent the browser default action so they can override shortcuts like "Mod-s".
    Wrap a callback with `ui.codemirror.KeyBinding(...)` to override that (`prevent_default=False`)
    or to provide per-platform shortcut overrides (`mac=`, `linux=`, `win=`).

    Use `unmap_key(key)` to remove a mapping at runtime.

    *Added in NiceGUI 3.14.0*
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
