from typing import Optional, Callable, Any

from ..element import Element
from ..events import handle_event, ScrollEventArguments


class ScrollArea(Element):

    def __init__(self, *,
                 on_scroll: Optional[Callable[..., Any]] = None) -> None:
        """Scroll Area

        A way of customizing the scrollbars by encapsulating your content.
        """
        super().__init__('q-scroll-area')
        self._classes = ['nicegui-scroll']

        def scroll_handle(info):
            handle_event(on_scroll, ScrollEventArguments(
                sender=self, client=self.client, info=info))

        if on_scroll:
            self.on('scroll', scroll_handle)
