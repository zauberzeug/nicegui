from pathlib import Path

from .. import helpers, json
from ..client import Client
from ..context import context
from ..slot import Slot


def add_css(content: str | Path, *, shared: bool = False) -> None:
    """Add CSS style definitions to the page.

    This function can be used to add CSS style definitions to the head of the HTML page.

    *Added in version 2.0.0*

    :param content: CSS content (string or file path)
    :param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)
    """
    if helpers.is_file(content):
        content = Path(content).read_text(encoding='utf-8')
    safe_content = json.dumps(content).replace('<', r'\u003c')
    _add_javascript(f'addStyle({safe_content});', shared=shared)


def add_scss(content: str | Path, *, indented: bool = False, shared: bool = False) -> None:  # DEPRECATED
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
    _add_javascript(f'''
        import("sass").then(sass => addStyle(sass.compileString({safe_content}, {{syntax: "{syntax}"}}).css));
    ''', shared=shared)


def add_sass(content: str | Path, *, shared: bool = False) -> None:  # DEPRECATED
    """Add SASS style definitions to the page (deprecated).

    This function can be used to add SASS style definitions to the head of the HTML page.

    *Added in version 2.0.0*

    **Note: This function is deprecated and will be removed in NiceGUI 4.0. Use add_css instead.**

    :param content: SASS content (string or file path)
    :param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)
    """
    add_scss(content, indented=True, shared=shared)


def _add_javascript(code: str, *, shared: bool = False) -> None:
    script_html = f'<script>{code}</script>'
    if shared:
        client = context.client if Slot.get_stack() else None  # NOTE: don't auto-create a client if shared=True
        Client.shared_head_html += script_html + '\n'
    else:
        client = context.client
        client._head_html += script_html + '\n'
    if client is not None and client.has_socket_connection:  # NOTE: no need to run JavaScript if there is no client yet
        client.run_javascript(code)
