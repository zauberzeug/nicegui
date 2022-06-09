from typing import Optional, Union

from justpy import WebPage
from nicegui.elements.page import Page
from starlette.websockets import WebSocket

from ..task_logger import create_task


def open(self, target: Union[Page, str], socket: Optional[WebSocket] = None):
    """
    Open

    Can be used to programmatically trigger redirects for a specific client.

    Note that *all* clients (i.e. browsers) connected to the page will open the target URL *unless* a socket is specified.
    User events like button clicks provide such a socket.

    :param target: page or string that is a an absolute URL or relative path from base URL
    :param socket: optional WebSocket defining the target client
    """
    create_task(open_async(self, target, socket), name='open_async')


async def open_async(self, target: Union[Page, str], socket: Optional[WebSocket] = None):
    path = target if isinstance(target, str) else target.route[1:]
    sockets = [socket] if socket else [s for socket_dict in WebPage.sockets.values() for s in socket_dict.values()]
    for socket in sockets:
        if not path:
            path = ' '  # NOTE empty string seems to be transformed to "null" when sending
        await socket.send_json({'type': 'page_update', 'page_options': {'redirect': path}})
