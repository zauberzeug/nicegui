from nicegui import ui

from . import doc


@doc.demo(ui.navigate)
def main_demo() -> None:
    ui.button('Back', on_click=ui.navigate.back)
    ui.button('Forward', on_click=ui.navigate.forward)
    ui.button('Navigate to', on_click=lambda: ui.navigate.to('/documentation'))
    ui.button('Update URL', on_click=lambda: ui.navigate.update('/random_page'))


@doc.demo(ui.navigate.to)
def open_github() -> None:
    url = 'https://github.com/zauberzeug/nicegui/'
    ui.button('Open GitHub', on_click=lambda: ui.navigate.to(url, new_tab=True))
