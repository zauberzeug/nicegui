from typing import Any, Callable, Union

from .. import globals


def open(target: Union[Callable[..., Any], str], new_tab: bool = False) -> None:
    """Open

    Can be used to programmatically trigger redirects for a specific client.

    Note that *all* clients (i.e. browsers) connected to the page will open the target URL *unless* a socket is specified.
    User events like button clicks provide such a socket.

    :param target: page function or string that is a an absolute URL or relative path from base URL
    :param new_tab: whether to open the target in a new tab
    """
    path = target if isinstance(target, str) else globals.page_routes[target]
    globals.get_client().open(path, new_tab)
