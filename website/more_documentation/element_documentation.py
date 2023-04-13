from nicegui import ui


def main_demo() -> None:
    with ui.element('div').classes('p-2 bg-blue-100'):
        ui.label('inside a colored div')
