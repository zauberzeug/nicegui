from nicegui import ui

from . import doc


@doc.demo(ui.content)
def main_demo() -> None:
    @ui.content('/spa')
    def spa_layout():
        with ui.header() as header:
            ui.label('Simple Single Page App').classes('text-2xl')
        yield {'header': header}
        ui.label('A footer added to each view.')

    @spa_layout.view('/', title='Home')
    def spa_index(header):
        ui.label('This is the home page of the Single Page App.')
        ui.button('Toggle header', on_click=lambda: header.toggle())
        ui.link('Go to other page', other_spa_page)

    @spa_layout.view('/other', title='Other Page')
    def other_spa_page():
        ui.label('Another page sharing the same layout.')
        ui.link('Go to index page', spa_index)
        ui.button('Navigate back', on_click=lambda: ui.navigate.back())

    ui.link('Open Single Page App', '/spa')
