from typing import Any, Callable, Union

from .. import context
from ..client import Client
from ..logging import log


def open(target: Union[Callable[..., Any], str], new_tab: bool = False) -> None:  # pylint: disable=redefined-builtin
    """Open

    Can be used to programmatically trigger redirects for a specific client.

    When using the `new_tab` parameter, the browser might block the new tab.
    This is a browser setting and cannot be changed by the application.
    You might want to use `ui.link` and its `new_tab` parameter instead.

    Note: When using an `auto-index page </documentation#auto-index_page>`_ (e.g. no `@page` decorator), 
    all clients (i.e. browsers) connected to the page will open the target URL unless a socket is specified.
    User events like button clicks provide such a socket.

    :param target: page function or string that is a an absolute URL or relative path from base URL
    :param new_tab: whether to open the target in a new tab (might be blocked by the browser)
    """
    path = target if isinstance(target, str) else Client.page_routes[target]
    client = context.get_client()
    if client.has_socket_connection:
        client.open(path, new_tab)
    else:
        log.error('Cannot open page because client is not connected, try RedirectResponse from FastAPI instead')
