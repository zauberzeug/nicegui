from collections import deque
from typing import Optional

from ..dependencies import register_component
from ..element import Element

register_component('log', __file__, 'log.js')


class Log(Element):

    def __init__(self, max_lines: Optional[int] = None) -> None:
        """Log view

        Create a log view that allows to add new lines without re-transmitting the whole history to the client.

        :param max_lines: maximum number of lines before dropping oldest ones (default: `None`)
        """
        super().__init__('log')
        self._props['max_lines'] = max_lines
        self._props['lines'] = ''
        self.classes('border whitespace-pre font-mono')
        self.style('opacity: 1 !important; cursor: text !important')
        self.lines: deque[str] = deque(maxlen=max_lines)

    def push(self, line: str) -> None:
        self.lines.extend(line.splitlines())
        self._props['lines'] = '\n'.join(self.lines)
        self.run_method('push', line)
