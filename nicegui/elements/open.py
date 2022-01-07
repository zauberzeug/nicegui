import asyncio
from .element import Element
from .custom_view import CustomView

class OpenView(CustomView):

    def __init__(self):
        super().__init__('open', __file__)
        self.initialize()

class Open(Element):

    def __init__(self, path: str, event_arguments=None):
        super().__init__(OpenView())
        if event_arguments:
            self.push(path, event_arguments)

    async def push_async(self, line: str, event_arguments):
        websocket = event_arguments.event.get('websocket')
        await self.view.run_method(f'redirect("{line}")', websocket)
        print('button was pressed. origin ' + str(websocket), flush=True)

    def push(self, line: str, e):
        asyncio.get_event_loop().create_task(self.push_async(line, e))
