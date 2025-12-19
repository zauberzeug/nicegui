from pathlib import Path
from typing import Union

from .. import helpers, json
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
    safe_content = json.dumps(content).replace('<', r'\u003c')
    add_head_html(f'<script>addStyle({safe_content});</script>', shared=shared)


def add_scss(content: Union[str, Path], *, indented: bool = False, shared: bool = False) -> None:  # DEPRECATED
    """Add SCSS style definitions to the page (deprecated).

    This function can be used to add SCSS style definitions to the head of the HTML page.

    *Added in version 2.0.0*

    **Note: This function is deprecated and will be removed in NiceGUI 4.0. Use add_css instead.**

    :param content: SCSS content (string or file path)
    :param indented: whether the content is indented (SASS) or not (SCSS) (default: `False`)
    :param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)
    """
    content = Path(content).read_text(encoding='utf-8') if helpers.is_file(content) else str(content).strip()
    syntax = 'indented' if indented else 'scss'
    safe_content = json.dumps(content).replace('<', r'\u003c')
    add_head_html(f'''
        <script type="module">
            import * as sass from "sass";
            addStyle(sass.compileString({safe_content}, {{syntax: "{syntax}"}}).css);
        </script>
    ''', shared=shared)


def add_sass(content: Union[str, Path], *, shared: bool = False) -> None:  # DEPRECATED
    """Add SASS style definitions to the page (deprecated).

    This function can be used to add SASS style definitions to the head of the HTML page.

    *Added in version 2.0.0*

    **Note: This function is deprecated and will be removed in NiceGUI 4.0. Use add_css instead.**

    :param content: SASS content (string or file path)
    :param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)
    """
    add_scss(content, indented=True, shared=shared)
