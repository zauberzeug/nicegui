from nicegui import ui


def main_demo() -> None:
    with ui.row():
        ui.spinner(size='lg')
        ui.spinner('audio', size='lg', color='green')
        ui.spinner('dots', size='lg', color='red')
