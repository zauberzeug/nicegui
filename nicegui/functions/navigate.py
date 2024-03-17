from typing import Any, Callable, Union

from .. import context
from ..client import Client
from ..element import Element
from .javascript import run_javascript


class Navigate:
    """Navigation functions

    These functions allow you to navigate within the browser history and to external URLs.
    """

    @staticmethod
    def back() -> None:
        """ui.navigate.back

        Navigates back in the browser history.
        It is equivalent to clicking the back button in the browser.
        """
        run_javascript('history.back()')

    @staticmethod
    def forward() -> None:
        """ui.navigate.forward

        Navigates forward in the browser history.
        It is equivalent to clicking the forward button in the browser.
        """
        run_javascript('history.forward()')

    @staticmethod
    def reload() -> None:
        """ui.navigate.reload

        Reload the current page.
        It is equivalent to clicking the reload button in the browser.
        """
        run_javascript('history.go(0)')

    @staticmethod
    def to(target: Union[Callable[..., Any], str, Element], new_tab: bool = False) -> None:
        """ui.navigate.to (formerly ui.open)

        Can be used to programmatically open a different page or URL.

        When using the `new_tab` parameter, the browser might block the new tab.
        This is a browser setting and cannot be changed by the application.
        You might want to use `ui.link` and its `new_tab` parameter instead.

        This functionality was previously available as `ui.open` which is now deprecated.

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
