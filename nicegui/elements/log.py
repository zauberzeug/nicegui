from typing import Any, Optional

from ..element import Element
from .label import Label


class Log(Element, default_classes='nicegui-log'):

    def __init__(self, max_lines: Optional[int] = None) -> None:
        """Log View

        Create a log view that allows to add new lines without re-transmitting the whole history to the client.

        :param max_lines: maximum number of lines before dropping oldest ones (default: `None`)
        """
        super().__init__()
        self.max_lines = max_lines

    def push(self, line: Any) -> None:
        """Add a new line to the log.

        :param line: the line to add (can contain line breaks)
        """
        for text in str(line).splitlines():
            with self:
                Label(text)
        while self.max_lines is not None and len(self.default_slot.children) > self.max_lines:
            self.remove(0)
