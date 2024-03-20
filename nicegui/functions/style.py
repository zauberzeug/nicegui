from pathlib import Path
from typing import Union

import sass

from .. import helpers
from .html import add_head_html


def add_style(content: Union[str, Path], indented: bool = False) -> None:
    """Add style definitions to the page.

    This function can be used to add CSS, SCSS, or SASS style definitions to the head of the HTML page.

    :param content: style content (string or file path)
    :param indented: whether the content is indented (SASS) or not (SCSS/CSS) (default: `False`)
    """
    if helpers.is_file(content):
        content = Path(content).read_text()
    css = sass.compile(string=str(content).strip(), indented=indented)
    add_head_html(f'<style>{css}</style>')
