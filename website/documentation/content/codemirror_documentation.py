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
    Keys follow CodeMirror's [keymap syntax](https://codemirror.net/docs/ref/#view.KeyBinding) — use
    ``Mod`` for Cmd on macOS and Ctrl elsewhere.

    By default, bindings prevent the browser default action so they can override shortcuts like ``Mod-s``.
    Wrap a callback with ``ui.codemirror.binding(...)`` to override that (``prevent_default=False``)
    or to provide per-platform shortcut overrides (``mac=``, ``linux=``, ``win=``).

    Use ``remove_keybinding(key)`` to unbind at runtime.
''')
def keybindings_demo() -> None:
    status = ui.label('Click into the editor and press Mod-s, Mod-r, F5, Mod-c, or Mod-Shift-d.')
    editor = ui.codemirror(
        'def hello():\n    print("hi")',
        language='Python',
        keybindings={
            'Mod-s': lambda e: status.set_text(f'Saved! ({e.key})'),
            'Mod-r': lambda: status.set_text('Run!'),
            'F5': lambda: status.set_text('Refresh!'),
            'Mod-c': ui.codemirror.binding(
                lambda: status.set_text('Copy logged (browser still copies).'),
                prevent_default=False,
            ),
        },
    ).classes('h-32')
    editor.on_keybinding('Mod-Shift-d', lambda: status.set_text('Bound at runtime via on_keybinding.'))
    ui.button('Unbind F5', on_click=lambda: editor.remove_keybinding('F5'))


doc.reference(ui.codemirror)
