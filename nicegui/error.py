from nicegui import ui


def error_content(status_code: int, message: str = '') -> None:
    if 400 <= status_code <= 499:
        title = "This page doesn't exist"
    elif 500 <= status_code <= 599:
        title = 'Server error'
    else:
        title = 'Unknown error'

    with ui.column().classes('w-full py-20 items-center gap-0'):
        ui.icon('☹').classes('text-8xl py-5').style('font-family: "Arial Unicode MS", "Times New Roman", Times, serif;')
        ui.label(status_code).classes('text-6xl py-5')
        ui.label(title).classes('text-xl py-5')
        ui.label(message).classes('text-lg py-2 text-gray-500')
