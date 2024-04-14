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


def add_style(content: Union[str, Path], indented: bool = False) -> None:  # DEPRECATED
    """Add style definitions to the page. [DEPRECATED]

    Note:
    This function is deprecated, because it can't reliably detect the style language.
    Use `add_css`, `add_scss` or `add_sass` instead.
    """
    if helpers.is_file(content):
        content = Path(content).read_text()
    if optional_features.has('sass'):
        content = sass.compile(string=str(content).strip(), indented=indented)
    log.warning("`ui.add_style` is deprecated, because it can't reliably detect the style language. "
                'Use `ui.add_css`, `ui.add_scss` or `ui.add_sass` instead.')
    add_head_html(f'<style>{content}</style>')


def add_css(content: Union[str, Path]) -> None:
    """Add CSS style definitions to the page.

    This function can be used to add CSS style definitions to the head of the HTML page.

    :param content: CSS content (string or file path)
    """
    if helpers.is_file(content):
        content = Path(content).read_text()
    add_head_html(f'<style>{content}</style>')


def add_scss(content: Union[str, Path], *, indented: bool = False) -> None:
    """Add SCSS style definitions to the page.

    This function can be used to add SCSS style definitions to the head of the HTML page.

    :param content: SCSS content (string or file path)
    :param indented: whether the content is indented (SASS) or not (SCSS) (default: `False`)
    """
    if not optional_features.has('sass'):
        raise ImportError('Please run "pip install libsass" to use SASS or SCSS.')

    if helpers.is_file(content):
        content = Path(content).read_text()
    add_css(sass.compile(string=str(content).strip(), indented=indented))


def add_sass(content: Union[str, Path]) -> None:
    """Add SASS style definitions to the page.

    This function can be used to add SASS style definitions to the head of the HTML page.

    :param content: SASS content (string or file path)
    """
    add_scss(content, indented=True)
