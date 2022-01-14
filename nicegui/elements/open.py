import asyncio
from starlette.websockets import WebSocket


class Open:

    def __init__(self, path: str, socket: WebSocket):
        """
        Open

        Can be used to programmatically trigger redirects for a specific client.

        :param path: string that is a relative url path or an absolute url
        :param socket: WebSocket defining the target client
        """
        asyncio.get_event_loop().create_task(self.redirect_async(path, socket))

    @staticmethod
    async def redirect_async(path: str, socket: WebSocket):
        # Depends on the 'page_update' in the main.html.
        await socket.send_json({'type': 'page_update', 'page_options': {'redirect': path}})
        # So the page itself does not update, return True not None
        return True
