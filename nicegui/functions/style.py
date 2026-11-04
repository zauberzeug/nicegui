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


def _add_javascript(code: str, *, shared: bool = False) -> None:
    script_html = f'<script>{code}</script>'
    if shared:
        client = context.client if Slot.get_stack() else None  # don't auto-create a client if shared=True
        Client.shared_head_html += script_html + '\n'
    else:
        client = context.client
        client._head_html += script_html + '\n'
    if client is not None and client._response_built and not client.is_deleted:  # pylint: disable=protected-access
        client.run_javascript(code)
