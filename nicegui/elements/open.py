from starlette.websockets import WebSocket
from ..task_logger import create_task


def open(self, path: str, socket: WebSocket):
    """
    Open

    Can be used to programmatically trigger redirects for a specific client.

    :param path: string that is a relative URL path or an absolute URL
    :param socket: WebSocket defining the target client
    """
    create_task(open_async(self, path, socket))

async def open_async(self, path: str, socket: WebSocket):
    await socket.send_json({'type': 'page_update', 'page_options': {'redirect': path}})
