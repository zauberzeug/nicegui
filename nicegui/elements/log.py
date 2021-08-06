import asyncio
from justpy.htmlcomponents import WebPage
from .custom_view import CustomView
from .element import Element

class LogView(CustomView):

    def __init__(self):

        super().__init__('log', __file__)

class Log(Element):

    def __init__(self):

        super().__init__(LogView())

    async def push(self, line: str):

        await asyncio.gather(*[
            self.view.run_method(f'push("{line}")', socket)
            for socket in WebPage.sockets[Element.wp.page_id].values()
        ])
