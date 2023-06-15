import urllib.parse
from collections import deque
from typing import Any, Optional

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
        self._classes = ['nicegui-log']
        self.lines: deque[str] = deque(maxlen=max_lines)
        self.total_count: int = 0

    def push(self, line: Any) -> None:
        new_lines = [urllib.parse.quote(line) for line in str(line).splitlines()]
        self.lines.extend(new_lines)
        self._props['lines'] = '\n'.join(self.lines)
        self.total_count += len(new_lines)
        self.run_method('push', urllib.parse.quote(str(line)), self.total_count)

    def clear(self) -> None:
        """Clear the log"""
        super().clear()
        self._props['lines'] = ''
        self.lines.clear()
        self.run_method('clear')
