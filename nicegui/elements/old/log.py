from __future__ import annotations

import asyncio
import traceback
import urllib
from collections import deque
from typing import Deque

from justpy.htmlcomponents import WebPage

from ..routes import add_dependencies
from ..task_logger import create_task
from .custom_view import CustomView
from .element import Element

add_dependencies(__file__)


class LogView(CustomView):

    def __init__(self, lines: Deque[str], max_lines: int):
        super().__init__('log', max_lines=max_lines)
        self.lines = lines
        self.allowed_events = ['onConnect']
        self.initialize(onConnect=self.handle_connect)

    def handle_connect(self, msg):
        try:
            if self.lines:
                content = '\n'.join(self.lines)
                command = f'push("{urllib.parse.quote(content)}")'
                create_task(self.run_method(command, msg.websocket), name=str(command))
        except:
            traceback.print_exc()


class Log(Element):

    def __init__(self, max_lines: int = None):
        """Log view

        Create a log view that allows to add new lines without re-transmitting the whole history to the client.

        :param max_lines: maximum number of lines before dropping oldest ones (default: `None`)
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
        create_task(self.push_async(line), name=f'log.push line {line}')
