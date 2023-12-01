from nicegui import ui


def main_demo() -> None:
    with ui.row():
        ui.label('label 1')
        ui.label('label 2')
        ui.label('label 3')
