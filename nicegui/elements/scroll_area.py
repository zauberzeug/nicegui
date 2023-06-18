from ..element import Element


class ScrollArea(Element):

    def __init__(self) -> None:
        """ScrollArea

        A way of customizing the scrollbars by encapsulating your content.
        """
        super().__init__('q-scroll-area')
        self._classes = ['nicegui-scroll']
