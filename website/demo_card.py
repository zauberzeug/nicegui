from nicegui import ui

from .constants import STATIC


def create():
    with ui.row().style('filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1))'):
        with ui.card().style(f'clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%)') \
                .classes('pb-16 no-shadow'), ui.row().classes('no-wrap'):
            with ui.column().classes('items-center'):
                ui.html((STATIC / 'happy_face.svg').read_text()) \
                    .classes('w-16 mx-6 stroke-black').on('click', lambda _: output.set_text("That's my face!"))
                ui.button('Click me!', on_click=lambda: output.set_text('Clicked')).classes('w-full')
                ui.input('Text', value='abc', on_change=lambda e: output.set_text(e.value))
                ui.checkbox('Check', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))
                ui.switch('Switch', on_change=lambda e: output.set_text('Switched on' if e.value else 'Switched off'))

            with ui.column().classes('items-center'):
                output = ui.label('Try it out!') \
                    .classes('w-44 my-6 h-8 text-xl text-grey-9 overflow-hidden text-ellipsis text-center')
                ui.slider(min=0, max=100, value=50, step=0.1, on_change=lambda e: output.set_text(e.value)) \
                    .style('width: 150px; margin-bottom: 2px')
                with ui.row():
                    ui.number('Number', value=3.1415927, format='%.2f', on_change=lambda e: output.set_text(e.value)) \
                        .classes('w-20')
                    ui.select({1: 'One', 2: 'Two', 3: 'Three'}, value=1, on_change=lambda e: output.set_text(e.value))
                ui.toggle(['1', '2', '3'], value='1', on_change=lambda e: output.set_text(e.value))
                ui.radio(['A', 'B', 'C'], value='A', on_change=lambda e: output.set_text(e.value)).props('inline')
