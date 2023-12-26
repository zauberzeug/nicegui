from nicegui import ui

from . import doc


@doc.demo(ui.grid)
def main_demo() -> None:
    with ui.grid(columns=2):
        ui.label('Name:')
        ui.label('Tom')

        ui.label('Age:')
        ui.label('42')

        ui.label('Height:')
        ui.label('1.80m')


@doc.demo('Cells spanning multiple columns', '''
    This demo shows how to span cells over multiple columns.

    Note that there is [no Tailwind class for spanning 15 columns](https://tailwindcss.com/docs/grid-column),
    but we can set [arbitrary values](https://tailwindcss.com/docs/grid-column#arbitrary-values) using square brackets.
    Alternatively you could use the corresponding CSS definition: `.style('grid-column: span 15 / span 15')`.
''')
def span_demo() -> None:
    with ui.grid(columns=16).classes('w-full gap-0'):
        ui.label('full').classes('col-span-full border p-1')
        ui.label('8').classes('col-span-8 border p-1')
        ui.label('8').classes('col-span-8 border p-1')
        ui.label('12').classes('col-span-12 border p-1')
        ui.label('4').classes('col-span-4 border p-1')
        ui.label('15').classes('col-[span_15] border p-1')
        ui.label('1').classes('col-span-1 border p-1')


doc.reference(ui.grid)
