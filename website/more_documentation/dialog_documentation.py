from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    with ui.dialog() as dialog, ui.card():
        ui.label('Hello world!')
        ui.button('Close', on_click=dialog.close)

    ui.button('Open a dialog', on_click=dialog.open)


def more() -> None:
    @text_demo('Awaitable dialog', '''
        Dialogs can be awaited.
        Use the `submit` method to close the dialog and return a result.
        Canceling the dialog by clicking in the background or pressing the escape key yields `None`.
    ''')
    def async_dialog_demo():
        with ui.dialog() as dialog, ui.card():
            ui.label('Are you sure?')
            with ui.row():
                ui.button('Yes', on_click=lambda: dialog.submit('Yes'))
                ui.button('No', on_click=lambda: dialog.submit('No'))

        async def show():
            result = await dialog
            ui.notify(f'You chose {result}')

        ui.button('Await a dialog', on_click=show)

    @text_demo('Replacing content', '''
        The content of a dialog can be changed.
    ''')
    def replace_content():
        def replace():
            dialog.clear()
            with dialog, ui.card().classes('w-64 h-64'):
                ui.label('New Content')
            dialog.open()

        with ui.dialog() as dialog, ui.card():
            ui.label('Hello world!')

        ui.button('Open', on_click=dialog.open)
        ui.button('Replace', on_click=replace)
