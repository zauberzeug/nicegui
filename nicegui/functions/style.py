from pathlib import Path
from typing import Union

from .. import optional_features

try:
    import sass
    optional_features.register('sass')
except ImportError:
    pass

from .. import helpers
from ..logging import log
from .html import add_head_html


def add_style(content: Union[str, Path], indented: bool = False) -> None:
    """Add style definitions to the page.

    This function can be used to add CSS, SCSS, or SASS style definitions to the head of the HTML page.

    :param content: style content (string or file path)
    :param indented: whether the content is indented (SASS) or not (SCSS/CSS) (default: `False`)
    """
    if helpers.is_file(content):
        content = Path(content).read_text()
    if optional_features.has('sass'):
        css = sass.compile(string=str(content).strip(), indented=indented)
    else:
        css = content
        sass_features = ["$", "@mixin", "{&"]
        if any(feature in css for feature in sass_features):
            log.warning('SASS features detected in ui.add_style. Please run "pip install libsass".')

    add_head_html(f'<style>{css}</style>')
