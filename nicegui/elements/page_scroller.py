from ..context import context
from ..element import Element
from .page_sticky import PageSticky, PageStickyPositions


class PageScroller(PageSticky):

    def __init__(self,
                 position: PageStickyPositions = 'bottom-right',
                 x_offset: float = 0,
                 y_offset: float = 0,
                 *,
                 expand: bool = False,
                 scroll_offset: int = 1000,
                 duration: int = 300,
                 reverse: bool = False,
                 ) -> None:
        """Page scroller

        This element is based on Quasar's `QPageScroller <https://quasar.dev/layout/page-scroller>`_ component.

        It is very similar to ``ui.page_sticky``, sharing ``position``, ``x_offset``, and ``y_offset`` parameters.

        However, ``ui.page_sticky`` is always visible, and ``ui.page_scroller`` only appears after the ``scroll-offset`` is reached.

        Once visible, the user can click on it to quickly get back to the top of the page in ``duration`` ms.

        :param position: position on the screen (default: "bottom-right")
        :param x_offset: horizontal offset (default: 0)
        :param y_offset: vertical offset (default: 0)
        :param expand: whether to fully expand instead of shrinking to fit the content (default: ``False``)
        :param scroll_offset: the vertical offset in pixels at which the scroller becomes visible (default: 1000)
        :param duration: the duration in milliseconds for the scroll animation (default: 300)
        :param reverse: if True, the scroller will work in reverse, showing when at the top of the page, and scrolls to bottom when triggered (default: ``False``)
        """
        super().__init__(position=position, x_offset=x_offset, y_offset=y_offset, expand=expand)
        self.tag = 'q-page-scroller'
        self._props['scroll-offset'] = scroll_offset
        self._props['duration'] = duration
        if reverse:
            self._props['reverse'] = True


def _check_current_slot(element: Element) -> None:
    parent = context.slot.parent
    if parent != parent.client.content:
        raise RuntimeError(f'Found top level layout element "{element.__class__.__name__}" inside element "{parent.__class__.__name__}". '
                           'Top level layout elements can not be nested but must be direct children of the page content.')
