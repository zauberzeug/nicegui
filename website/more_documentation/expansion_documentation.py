from nicegui import ui


def main_demo() -> None:
    with ui.expansion('Expand!', icon='work').classes('w-full'):
        ui.label('inside the expansion')
