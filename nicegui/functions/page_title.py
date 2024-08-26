from .. import core, json
from ..context import context


def page_title(title: str) -> None:
    """Page title

    Set the page title for the current client.

    :param title: page title
    """
    client = context.client
    client.title = title
    if core.app.native.main_window:
        core.app.native.main_window.set_title(title)
    if client.has_socket_connection:
        client.run_javascript(f'document.title = {json.dumps(title)}')
