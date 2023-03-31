from nicegui import ui


def main_demo() -> None:
    from datetime import datetime

    log = ui.log(max_lines=10).classes('w-full h-20')
    ui.button('Log time', on_click=lambda: log.push(datetime.now().strftime('%X.%f')[:-5]))
