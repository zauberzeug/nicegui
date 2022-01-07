import asyncio
from .element import Element
from .custom_view import CustomView

class OpenView(CustomView):

    def __init__(self):
        super().__init__('open', __file__)

class Open(Element):

    def __init__(self):
        """
        Open Element

        Adds a global element to programmatically trigger redirects for a specific client.
        """
        super().__init__(OpenView())
        self.view.initialize()

    async def redirect_async(self, path: str, event_arguments):
        websocket = event_arguments.event.get('websocket')
        await self.view.run_method(f'redirect("{path}")', websocket)

    def redirect(self, path: str = None, event_arguments=None):
        asyncio.get_event_loop().create_task(self.redirect_async(path, event_arguments))

    __call__ = redirect
