from dataclasses import fields
from typing import Optional, Callable, Any, Dict

from ..element import Element
from ..events import ScrollEventArguments, ScrollInfo


class ScrollArea(Element):

    def __init__(self, *,
                 on_scroll: Optional[Callable[..., Any]] = None) -> None:
        """Scroll Area

        A way of customizing the scrollbars by encapsulating your content.
        """
        super().__init__('q-scroll-area')
        self._classes = ['nicegui-scroll']

        if on_scroll:
            self.on('scroll',
                    lambda x: self._handle_scroll(on_scroll=on_scroll, msg=x), args=[x.name for x in fields(ScrollInfo)]
                    )

    def _handle_scroll(self, on_scroll: Callable, msg: Dict):
        on_scroll(ScrollEventArguments(
            sender=self,
            client=self.client,
            info=ScrollInfo(**msg['args'])
        ))
