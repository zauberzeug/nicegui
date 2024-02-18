from typing import Any, Callable, Union

from .. import context
from ..client import Client
from ..element import Element


def open(target: Union[Callable[..., Any], str, Element], new_tab: bool = False) -> None:  # pylint: disable=redefined-builtin
    """Open

    Can be used to programmatically trigger redirects for a specific client.

    When using the `new_tab` parameter, the browser might block the new tab.
    This is a browser setting and cannot be changed by the application.
    You might want to use `ui.link` and its `new_tab` parameter instead.

    Note: When using an `auto-index page </documentation/section_pages_routing#auto-index_page>`_ (e.g. no `@page` decorator), 
    all clients (i.e. browsers) connected to the page will open the target URL unless a socket is specified.
    User events like button clicks provide such a socket.

    :param target: page function, NiceGUI element on the same page or string that is a an absolute URL or relative path from base URL
    :param new_tab: whether to open the target in a new tab (might be blocked by the browser)
    """
    if isinstance(target, str):
        path = target
    elif isinstance(target, Element):
        path = f'#c{target.id}'
    elif callable(target):
        path = Client.page_routes[target]
    context.get_client().open(path, new_tab)
