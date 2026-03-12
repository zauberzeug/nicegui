from typing import Any

from ..element import Element
from .label import Label


class Log(Element, component='log.js', default_classes='nicegui-log'):

    def __init__(self, max_lines: int | None = None) -> None:
        """Log View

        Create a log view that allows to add new lines without re-transmitting the whole history to the client.

        :param max_lines: maximum number of lines before dropping oldest ones (default: `None`)
        """
        super().__init__()
        self.max_lines = max_lines

    def push(self, line: Any, *,
             classes: str | None = None,
             style: str | None = None,
             props: str | None = None) -> None:
        """Add a new line to the log.

        :param line: the line to add (can contain line breaks)
        :param classes: classes to apply to the line (*added in version 2.18.0*)
        :param style: style to apply to the line (*added in version 2.18.0*)
        :param props: props to apply to the line (*added in version 2.18.0*)
        """
        for text in str(line).splitlines():
            with self:
                label = Label(text)
                if classes is not None:
                    label.classes(replace=classes)
                if style is not None:
                    label.style(replace=style)
                if props is not None:
                    label.props.clear()
                    label.props(props)
        while self.max_lines is not None and len(self.default_slot.children) > self.max_lines:
            self.remove(0)
