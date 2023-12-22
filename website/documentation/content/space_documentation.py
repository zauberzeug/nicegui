from nicegui import ui

from . import doc


@doc.demo(ui.space)
def main_demo() -> None:
    with ui.row().classes('w-full border'):
        ui.label('Left')
        ui.space()
        ui.label('Right')


@doc.demo('Vertical space', '''
    This element can also be used to fill vertical space.
''')
def vertical_demo() -> None:
    with ui.column().classes('h-32 border'):
        ui.label('Top')
        ui.space()
        ui.label('Bottom')


doc.reference(ui.space)
