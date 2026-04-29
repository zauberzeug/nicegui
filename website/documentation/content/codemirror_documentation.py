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
    The browser tracks each anchor's position through every change — insertions, deletions,
    reformatting — and ``line_anchor_positions`` mirrors the current line on the Python side.
    The example below attaches anchor "A" and "B" to the two lines and lets you rewrite either
    one in place: edit the code freely (add blank lines, indent, reorder), then click "Update"
    — the right line gets rewritten because the anchor followed the line.
''')
def line_anchors_demo() -> None:
    code = (
        'rbt.move_l([100.0, 0.0, 200.0])\n'
        'rbt.move_l([100.0, 100.0, 200.0])\n'
    )
    editor = ui.codemirror(code, language='Python').classes('h-40')
    editor.set_line_anchors([{'id': 'A', 'line': 1}, {'id': 'B', 'line': 2}])
    status = ui.label()

    def show_positions(_=None) -> None:
        pos = editor.line_anchor_positions.get('default', {})
        status.set_text(f'target A is on line {pos.get("A", "?")}, target B is on line {pos.get("B", "?")}')

    editor.on('anchor-positions', show_positions)
    show_positions()

    def update_target(target_id: str, new_pose: str) -> None:
        pos = editor.line_anchor_positions.get('default', {})
        line_no = pos.get(target_id)
        if not line_no:
            return
        lines = (editor.value or '').split('\n')
        if 0 < line_no <= len(lines):
            lines[line_no - 1] = f'rbt.move_l([{new_pose}])'
            editor.value = '\n'.join(lines)

    with ui.row():
        ui.button('Update target A', on_click=lambda: update_target('A', '50.0, -50.0, 150.0'))
        ui.button('Update target B', on_click=lambda: update_target('B', '150.0, 200.0, 250.0'))


doc.reference(ui.codemirror)
