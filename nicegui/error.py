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

    with ui.column().style('width: 100%; padding: 5rem 0; align-items: center; gap: 0'):
        ui.html((Path(__file__).parent / 'static' / 'sad_face.svg').read_text()).style('width: 8rem; padding: 1.25rem 0')
        ui.label(str(status_code)).style('font-size: 3.75rem; line-height: 1; padding: 1.25rem 0')
        ui.label(title).style('font-size: 1.25rem; line-height: 1.75rem; padding: 1.25rem 0')
        ui.label(message).style('font-size: 1.125rem; line-height: 1.75rem; color: rgb(107 114 128)')
