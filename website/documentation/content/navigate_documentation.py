from nicegui import ui

from . import doc


@doc.demo(ui.navigate)
def main_demo() -> None:
    with ui.row():
        ui.button('Back', on_click=ui.navigate.back)
        ui.button('Forward', on_click=ui.navigate.forward)
        ui.button(icon='savings',
                  on_click=lambda: ui.navigate.to('https://github.com/sponsors/zauberzeug'))


@doc.demo(ui.navigate.to)
def open_github() -> None:
    url = 'https://github.com/zauberzeug/nicegui/'
    ui.button('Open GitHub', on_click=lambda: ui.navigate.to(url, new_tab=True))
