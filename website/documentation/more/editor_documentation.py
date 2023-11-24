from nicegui import ui

from ..model import UiElementDocumentation


class EditorDocumentation(UiElementDocumentation, element=ui.editor):

    def main_demo(self) -> None:
        editor = ui.editor(placeholder='Type something here')
        ui.markdown().bind_content_from(editor, 'value',
                                        backward=lambda v: f'HTML code:\n```\n{v}\n```')
