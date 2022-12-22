from pathlib import Path
from typing import Union

from nicegui import ui


def error_content(status_code: int, exception: Union[str, Exception] = '') -> None:
    if 400 <= status_code <= 499:
        title = "This page doesn't exist."
    elif 500 <= status_code <= 599:
        title = 'Server error'
    else:
        title = 'Unknown error'

    if isinstance(exception, str):
        message = exception
    else:
        message = exception.__class__.__name__
        if str(exception):
            message += ': ' + str(exception)

    with ui.column().classes('w-full py-20 items-center gap-0'):
        ui.html((Path(__file__).parent / 'static' / 'sad_face.svg').read_text()).classes('w-32 py-5')
        ui.label(str(status_code)).classes('text-6xl py-5')
        ui.label(title).classes('text-xl py-5')
        ui.label(message).classes('text-lg text-gray-500')
