from dataclasses import fields
from typing import Optional, Callable, Any, Dict, Union, Literal

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

    def set_scroll_position(self, offset: Union[int, float], *,
                            axis: Literal['vertical', 'horizontal'] = 'vertical', duration_ms: int = 0
                            ) -> None:
        """

        :param offset: Scroll position offset from top in pixels or percentage (0.0 <= x <= 1.0) of the total scrolling
                        size
        :param axis: Scroll axis to set
        :param duration_ms: Duration (in milliseconds) enabling animated scroll
        """
        if offset < 0:
            raise ValueError(f'scroll offset must be positive. Got: {offset}')

        if type(offset) == int:
            self.run_method('setScrollPosition', axis, offset, duration_ms)

        elif type(offset) == float and offset > 1.0:
            raise ValueError(f'a percentage scroll offset must be 0.0 <= x <= 1.0. Got: {offset}')

        elif type(offset) == float and offset <= 1.0:
            self.run_method('setScrollPercentage', axis, offset, duration_ms)

        else:
            raise ValueError(f'Got unsupported offset: {offset}')
