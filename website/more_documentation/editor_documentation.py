from nicegui import ui


def main_demo() -> None:
    editor = ui.editor(placeholder='Type something here')
    ui.markdown().bind_content_from(editor, 'value',
                                    backward=lambda v: f'HTML code:\n```\n{v}\n```')
