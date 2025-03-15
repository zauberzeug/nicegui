from pathlib import Path
from typing import Union

from .elements.column import Column as column
from .elements.html import Html as html
from .elements.label import Label as label
from .elements.textarea import Textarea as textarea
from .elements.button import Button as button
from .elements.mixins.name_element import Element as element
from .elements.code import Code as code


import traceback

SAD_FACE_SVG = (Path(__file__).parent / 'static' / 'sad_face.svg').read_text()


def error_content(status_code: int, exception: Union[str, Exception] = '') -> None:
    """Create an error page.

    :param status_code: HTTP status code
    :param exception: exception that caused the error
    """
    if 400 <= status_code <= 499:
        title = "This page doesn't exist."
    elif 500 <= status_code <= 599:
        title = 'Server error'
    else:
        title = 'Unknown error'

    if isinstance(exception, str):
        message = exception
        message2 = ''
    else:
        message = exception.__class__.__name__
        message2 = traceback.format_exc(chain=False)
        if str(exception):
            message += ': ' + str(exception)
            message2 = message2.rpartition(message)[0].strip()
        # drop lines in traceback if they belong to NiceGUI
        message2 = '\n'.join(message2.split('\n')[:1] + message2.split('\n')[4:])

    with column().style('width: 100%; padding: 5rem 0; align-items: center; gap: 0'):
        html(SAD_FACE_SVG).style('width: 8rem; padding: 1.25rem 0')
        label(str(status_code)).style('font-size: 3.75rem; line-height: 1; padding: 1.25rem 0')
        label(title).style('font-size: 1.25rem; line-height: 1.75rem; padding: 1.25rem 0')
        label(message).style('font-size: 1.125rem; line-height: 1.75rem; color: rgb(107 114 128)')
        if message2:
            button("Show details").on('click', js_handler='() => {document.querySelector(".error-details").style.display = "block"; document.querySelector(".show-details").style.display = "none"; document.querySelector(".hide-details").style.display = "inline-block"}').style(
                'margin-top: 1rem').classes("show-details")
            button("Hide details").on('click', js_handler='() => {document.querySelector(".error-details").style.display = "none"; document.querySelector(".show-details").style.display = "inline-block"; document.querySelector(".hide-details").style.display = "none"}').style(
                'margin-top: 1rem; display: none').classes("hide-details")
            code(message2).style(
                'margin-top: 1rem; width: 100%; height: 20vh; overflow-y: auto; display: none').classes("error-details")
