from ..defaults import DEFAULT_PROP, resolve_defaults
from ..element import Element
from .page_sticky import PageStickyPositions


class PageScroller(Element):

    @resolve_defaults
    def __init__(self,
                 position: PageStickyPositions = DEFAULT_PROP | 'bottom-right',
                 x_offset: float = 0,
                 y_offset: float = 0,
                 *,
                 expand: bool = DEFAULT_PROP | False,
                 scroll_offset: float = DEFAULT_PROP | 1000,
                 duration: float = DEFAULT_PROP | 0.3,
                 reverse: bool = DEFAULT_PROP | False,
                 ) -> None:
        """Page scroller

        This element is based on Quasar's `QPageScroller <https://quasar.dev/layout/page-scroller>`_ component.

        It is very similar to ``ui.page_sticky``, sharing ``position``, ``x_offset``, ``y_offset``, and ``expand`` parameters.

        However, ``ui.page_sticky`` is always visible, and ``ui.page_scroller`` only appears after the ``scroll-offset`` is reached.

        Once visible, the user can click on it to quickly get back to the top of the page in ``duration`` seconds.

        *Added in version 3.3.0*

        :param position: position on the screen (default: "bottom-right")
        :param x_offset: horizontal offset (default: 0)
        :param y_offset: vertical offset (default: 0)
        :param expand: whether to fully expand instead of shrinking to fit the content (default: ``False``)
        :param scroll_offset: the vertical offset in pixels at which the scroller becomes visible (default: 1000)
        :param duration: the duration in seconds for the scroll animation (default: 0.3)
        :param reverse: if True, the scroller will work in reverse, showing when at the top of the page, and scrolls to bottom when triggered (default: ``False``)
        """
        super().__init__('q-page-scroller')
        self._props['position'] = position
        self._props['offset'] = [x_offset, y_offset]
        self._props['scroll-offset'] = scroll_offset
        self._props['duration'] = duration * 1000
        self._props.set_bool('expand', expand)
        self._props.set_bool('reverse', reverse)
