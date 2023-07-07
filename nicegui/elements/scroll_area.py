from typing import Any, Callable, Dict, Optional

from typing_extensions import Literal

from ..element import Element
from ..events import ScrollEventArguments, handle_event


class ScrollArea(Element):

    def __init__(self, *, on_scroll: Optional[Callable[..., Any]] = None) -> None:
        """Scroll Area

        A way of customizing the scrollbars by encapsulating your content.
        This element exposes the Quasar `ScrollArea <https://quasar.dev/vue-components/scroll-area/>`_ component.

        :param on_scroll: function to be called when the scroll position changes
        """
        super().__init__('q-scroll-area')
        self._classes = ['nicegui-scroll-area']

        if on_scroll:
            self.on('scroll', lambda msg: self._handle_scroll(on_scroll, msg), args=[
                'verticalPosition',
                'verticalPercentage',
                'verticalSize',
                'verticalContainerSize',
                'horizontalPosition',
                'horizontalPercentage',
                'horizontalSize',
                'horizontalContainerSize',
            ])

    def _handle_scroll(self, on_scroll: Callable[..., Any], msg: Dict) -> None:
        handle_event(on_scroll, ScrollEventArguments(
            sender=self,
            client=self.client,
            vertical_position=msg['args']['verticalPosition'],
            vertical_percentage=msg['args']['verticalPercentage'],
            vertical_size=msg['args']['verticalSize'],
            vertical_container_size=msg['args']['verticalContainerSize'],
            horizontal_position=msg['args']['horizontalPosition'],
            horizontal_percentage=msg['args']['horizontalPercentage'],
            horizontal_size=msg['args']['horizontalSize'],
            horizontal_container_size=msg['args']['horizontalContainerSize'],
        ))

    def scroll_to(self, *,
                  pixels: Optional[float] = None,
                  percent: Optional[float] = None,
                  axis: Literal['vertical', 'horizontal'] = 'vertical',
                  duration: float = 0.0,
                  ) -> None:
        """Set the scroll area position in percentage (float) or pixel number (int).

        You can add a delay to the actual scroll action with the `duration_ms` parameter.

        :param pixels: scroll position offset from top in pixels
        :param percent: scroll position offset from top in percentage of the total scrolling size
        :param axis: scroll axis
        :param duration: animation duration (in seconds, default: 0.0 means no animation)
        """
        if pixels is not None and percent is not None:
            raise ValueError('You can only specify one of pixels or percent')
        if pixels is not None:
            self.run_method('setScrollPosition', axis, pixels, 1000 * duration)
        elif percent is not None:
            self.run_method('setScrollPercentage', axis, percent, 1000 * duration)
        else:
            raise ValueError('You must specify one of pixels or percent')
