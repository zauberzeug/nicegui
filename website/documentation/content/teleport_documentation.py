from nicegui import ui

from . import doc


@doc.demo(ui.teleport)
def main_demo() -> None:
    markdown = ui.markdown('Enter your **name**!')

    def inject_input():
        with ui.teleport(f'#c{markdown.id} strong'):
            ui.input('name').classes('inline-flex').props('dense outlined')

    ui.button('inject input', on_click=inject_input)


doc.reference(ui.teleport)
