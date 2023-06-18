from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    with ui.row():
        with ui.card().classes('w-32 h-32'):
            ui.label('I will not scroll...\n' * 5)
        with ui.card().classes('w-32 h-32'):
            with ui.scroll_area().classes('w-full'):
                ui.label('I will scroll...\n' * 5)


def more() -> None:

    @text_demo('placeholder', '''
        ...
    ''')
    async def placeholder():
        ...
