from typing import Optional, Union

from justpy import WebPage
from nicegui.elements.page import Page
from starlette.websockets import WebSocket

from ..task_logger import create_task


def open(self, target: Union[Page, str], socket: Optional[WebSocket] = None):
    """
    Open

    Can be used to programmatically trigger redirects for a specific client.

    :param target: page or string that is a relative URL path or an absolute URL
    :param socket: optional WebSocket defining the target client
    """
    create_task(open_async(self, target, socket), name='open_async')


async def open_async(self, target: Union[Page, str], socket: Optional[WebSocket] = None):
    path = target if isinstance(target, str) else target.route
    sockets = [socket] if socket else [s for socket_dict in WebPage.sockets.values() for s in socket_dict.values()]
    for socket in sockets:
        await socket.send_json({'type': 'page_update', 'page_options': {'redirect': path}})
