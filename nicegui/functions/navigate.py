from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

from .. import background_tasks, json
from ..client import Client
from ..context import context
from ..element import Element
from ..elements.sub_pages import SubPages
from .javascript import run_javascript


class Navigate:
    """Navigation functions

    These functions allow you to navigate within the browser history and to external URLs.

    *Added in version 2.0.0*
    """

    def __init__(self) -> None:
        self.history = History()

    def back(self) -> None:
        """ui.navigate.back

        Navigates back in the browser history.
        It is equivalent to clicking the back button in the browser.
        """
        run_javascript('history.back()')

    def forward(self) -> None:
        """ui.navigate.forward

        Navigates forward in the browser history.
        It is equivalent to clicking the forward button in the browser.
        """
        run_javascript('history.forward()')

    def reload(self) -> None:
        """ui.navigate.reload

        Reload the current page.
        It is equivalent to clicking the reload button in the browser.
        """
        run_javascript('history.go(0)')

    def to(self, target: Callable[..., Any] | str | Element, new_tab: bool = False) -> None:
        """ui.navigate.to (formerly ui.open)

        Can be used to programmatically open a different page or URL.

        When using the `new_tab` parameter, the browser might block the new tab.
        This is a browser setting and cannot be changed by the application.
        You might want to use `ui.link` and its `new_tab` parameter instead.

        :param target: page function, NiceGUI element on the same page or string that is a an absolute URL or relative path from base URL
        :param new_tab: whether to open the target in a new tab (might be blocked by the browser)
        """
        if isinstance(target, str):
            path = target
        elif isinstance(target, Element):
            path = f'#{target.html_id}'
        elif callable(target):
            path = Client.page_routes[target]
        else:
            raise TypeError(f'Invalid target type: {type(target)}')

        if not new_tab and isinstance(target, str):
            parsed = urlparse(path)
            if not parsed.scheme and not parsed.netloc and \
                    any(isinstance(el, SubPages) for el in context.client.elements.values()):
                async def navigate_sub_pages(client: Client) -> None:
                    with client:
                        await client.sub_pages_router._handle_navigate(path)  # pylint: disable=protected-access
                background_tasks.create(navigate_sub_pages(context.client), name='navigate_sub_pages')
                return

        context.client.open(path, new_tab)


class History:

    def push(self, url: str) -> None:
        """Push a URL to the browser navigation history.

        See JavaScript's `pushState <https://developer.mozilla.org/en-US/docs/Web/API/History/pushState>`_ for more information.

        *Added in version 2.13.0*

        :param url: relative or absolute URL
        """
        run_javascript(f'history.pushState({{}}, "", {json.dumps(url)});')

    def replace(self, url: str) -> None:
        """Replace the current URL in the browser history.

        See JavaScript's `replaceState <https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState>`_ for more information.

        *Added in version 2.13.0*

        :param url: relative or absolute URL
        """
        run_javascript(f'history.replaceState({{}}, "", {json.dumps(url)});')


navigate = Navigate()
