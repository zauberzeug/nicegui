from typing import Literal

from typing_extensions import Self

from ..element import Element
from ..events import GenericEventArguments, Handler, ScrollEventArguments, handle_event


class ScrollArea(Element, default_classes='nicegui-scroll-area'):

    def __init__(self, *, on_scroll: Handler[ScrollEventArguments] | None = None) -> None:
        """Scroll Area

        A way of customizing the scrollbars by encapsulating your content.
        This element exposes the Quasar `ScrollArea <https://quasar.dev/vue-components/scroll-area/>`_ component.

        :param on_scroll: function to be called when the scroll position changes
        """
        super().__init__('q-scroll-area')

        if on_scroll:
            self.on_scroll(on_scroll)

    def on_scroll(self, callback: Handler[ScrollEventArguments]) -> Self:
        """Add a callback to be invoked when the scroll position changes."""
        self.on('scroll', lambda e: self._handle_scroll(callback, e), args=[
            'verticalPosition',
            'verticalPercentage',
            'verticalSize',
            'verticalContainerSize',
            'horizontalPosition',
            'horizontalPercentage',
            'horizontalSize',
            'horizontalContainerSize',
        ])
        return self

    def _handle_scroll(self, handler: Handler[ScrollEventArguments] | None, e: GenericEventArguments) -> None:
        handle_event(handler, ScrollEventArguments(
            sender=self,
            client=self.client,
            vertical_position=e.args['verticalPosition'],
            vertical_percentage=e.args['verticalPercentage'],
            vertical_size=e.args['verticalSize'],
            vertical_container_size=e.args['verticalContainerSize'],
            horizontal_position=e.args['horizontalPosition'],
            horizontal_percentage=e.args['horizontalPercentage'],
            horizontal_size=e.args['horizontalSize'],
            horizontal_container_size=e.args['horizontalContainerSize'],
        ))

    def scroll_to(self, *,
                  pixels: float | None = None,
                  percent: float | None = None,
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
