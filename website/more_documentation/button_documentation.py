from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.button('Click me!', on_click=lambda: ui.notify(f'You clicked me!'))


def more() -> None:
    @text_demo('Icons', '''
        You can also add an icon to a button.
    ''')
    async def icons() -> None:
        with ui.row():
            ui.button('demo').props('icon=history')
            ui.button().props('icon=thumb_up')
            with ui.button():
                ui.label('sub-elements')
                ui.image('https://picsum.photos/id/377/640/360') \
                    .classes('rounded-full w-16 h-16 ml-4 shadow-inner')

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
