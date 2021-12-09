import asyncio
import traceback
import urllib
from collections import deque
from justpy.htmlcomponents import WebPage
from .custom_view import CustomView
from .element import Element

class LogView(CustomView):

    def __init__(self, lines: deque[str], max_lines: int):
        super().__init__('log', __file__, max_lines=max_lines)
        self.lines = lines
        self.allowed_events = ['onConnect']
        self.initialize(onConnect=self.handle_connect)

    def handle_connect(self, msg):
        try:
            if self.lines:
                content = '\n'.join(self.lines)
                command = f'push("{urllib.parse.quote(content)}")'
                asyncio.get_event_loop().create_task(self.run_method(command, msg.websocket))
        except:
            traceback.print_exc()

class Log(Element):

    def __init__(self, max_lines: int = None):
        """Log view

        Create a log view that allows to add new lines without re-transmitting the whole history to the client.

        :param max_lines: maximum number of lines before dropping oldest ones (default: None)
        """
        self.lines = deque(maxlen=max_lines)
        super().__init__(LogView(lines=self.lines, max_lines=max_lines))
        self.classes('border whitespace-pre font-mono').style('opacity: 1 !important; cursor: text !important')

    async def push_async(self, line: str):
        self.lines.append(line)
        await asyncio.gather(*[
            self.view.run_method(f'push("{urllib.parse.quote(line)}")', socket)
            for socket in WebPage.sockets.get(self.page.page_id, {}).values()
        ])

    def push(self, line: str):
        asyncio.get_event_loop().create_task(self.push_async(line))
