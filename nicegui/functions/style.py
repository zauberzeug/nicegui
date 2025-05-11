from pathlib import Path
from typing import Union

from .. import optional_features

try:
    import sass
    optional_features.register('sass')
except ImportError:
    pass

from .. import helpers
from .html import add_head_html


def add_css(content: Union[str, Path], *, shared: bool = False) -> None:
    """Add CSS style definitions to the page.

    This function can be used to add CSS style definitions to the head of the HTML page.

    *Added in version 2.0.0*

    :param content: CSS content (string or file path)
    :param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)
    """
    if helpers.is_file(content):
        content = Path(content).read_text(encoding='utf-8')
    add_head_html(f'<style>{content}</style>', shared=shared)


def add_scss(content: Union[str, Path], *, indented: bool = False, shared: bool = False) -> None:
    """Add SCSS style definitions to the page.

    This function can be used to add SCSS style definitions to the head of the HTML page.

    *Added in version 2.0.0*

    :param content: SCSS content (string or file path)
    :param indented: whether the content is indented (SASS) or not (SCSS) (default: `False`)
    :param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)
    """
    if not optional_features.has('sass'):
        raise ImportError('Please run "pip install libsass" to use SASS or SCSS.')

    if helpers.is_file(content):
        content = Path(content).read_text(encoding='utf-8')
    add_css(sass.compile(string=str(content).strip(), indented=indented), shared=shared)


def add_sass(content: Union[str, Path], *, shared: bool = False) -> None:
    """Add SASS style definitions to the page.

    This function can be used to add SASS style definitions to the head of the HTML page.

    *Added in version 2.0.0*

    :param content: SASS content (string or file path)
    :param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)
    """
    add_scss(content, indented=True, shared=shared)
