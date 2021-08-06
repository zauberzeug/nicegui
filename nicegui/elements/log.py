import asyncio
import urllib
from justpy.htmlcomponents import WebPage
from .custom_view import CustomView
from .element import Element

class LogView(CustomView):

    def __init__(self, max_lines: int):

        super().__init__('log', __file__, max_lines=max_lines)

class Log(Element):

    def __init__(self, max_lines: int = None):
        """Log view

        Create a log view that allows to add new lines without re-transmitting the whole history to the client.

        :param max_lines: maximum number of lines before dropping oldest ones (default: None)
        """

        super().__init__(LogView(max_lines=max_lines))

        self.classes('border whitespace-pre font-mono').style('opacity: 1 !important; cursor: text !important')

    async def push_async(self, line: str):

        await asyncio.gather(*[
            self.view.run_method(f'push("{urllib.parse.quote(line)}")', socket)
            for socket in WebPage.sockets[Element.wp.page_id].values()
        ])

    def push(self, line: str):

        asyncio.get_event_loop().create_task(self.push_async(line))
