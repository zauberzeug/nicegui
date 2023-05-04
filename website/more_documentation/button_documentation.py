from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.button('Click me!', on_click=lambda: ui.notify(f'You clicked me!'))


def more() -> None:
    @text_demo('Await button click', '''
        Sometimes it is convenient to wait for a button click before continuing the execution.
    ''')
    async def await_button_click() -> None:
        # @ui.page('/')
        # async def index():
            b = ui.button('Step')
            await b.clicked()
            ui.label('One')
            await b.clicked()
            ui.label('Two')
            await b.clicked()
            ui.label('Three')
