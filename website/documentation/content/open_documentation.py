from nicegui import ui

from . import doc


@doc.demo(ui.open)
def main_demo() -> None:
    @ui.page('/yet_another_page')
    def yet_another_page():
        ui.label('Welcome to yet another page')
        ui.button('RETURN', on_click=lambda: ui.open('documentation#open'))

    ui.button('REDIRECT', on_click=lambda: ui.open(yet_another_page))
