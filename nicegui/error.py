from pathlib import Path
from typing import Union

from .elements.column import Column as column
from .elements.html import Html as html
from .elements.label import Label as label

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
    else:
        message = exception.__class__.__name__
        if str(exception):
            message += ': ' + str(exception)

    with column().style('width: 100%; padding: 5rem 0; align-items: center; gap: 0'):
        html(SAD_FACE_SVG).style('width: 8rem; padding: 1.25rem 0')
        label(str(status_code)).style('font-size: 3.75rem; line-height: 1; padding: 1.25rem 0')
        label(title).style('font-size: 1.25rem; line-height: 1.75rem; padding: 1.25rem 0')
        label(message).style('font-size: 1.125rem; line-height: 1.75rem; color: rgb(107 114 128)')
