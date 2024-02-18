from nicegui import ui

from . import doc


@doc.demo(ui.column)
def main_demo() -> None:
    with ui.column():
        ui.label('label 1')
        ui.label('label 2')
        ui.label('label 3')


@doc.demo('Masonry or Pinterest-Style Layout', '''
    To create a masonry/Pinterest layout, the normal `ui.column` can not be used.
    But it can be achieved with a few TailwindCSS classes.
''')
def masonry() -> None:
    with ui.element('div').classes('columns-3 w-full gap-2'):
        for i, height in enumerate([50, 50, 50, 150, 100, 50]):
            tailwind = f'mb-2 p-2 h-[{height}px] bg-blue-100 break-inside-avoid'
            with ui.card().classes(tailwind):
                ui.label(f'Card #{i+1}')


doc.reference(ui.column)
