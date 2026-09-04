from typing import Literal

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..element import Element

PageStickyPositions = Literal[
    'top-right',
    'top-left',
    'bottom-right',
    'bottom-left',
    'top',
    'right',
    'bottom',
    'left',
]


class PageSticky(Element):

    @resolve_defaults
    def __init__(self,
                 position: PageStickyPositions = DEFAULT_PROP | 'bottom-right',
                 x_offset: float = 0,
                 y_offset: float = 0,
                 *,
                 expand: bool = DEFAULT_PROP | False,
                 ) -> None:
        """Page sticky

        This element is based on Quasar's `QPageSticky <https://quasar.dev/layout/page-sticky>`_ component.

        :param position: position on the screen (default: "bottom-right")
        :param x_offset: horizontal offset (default: 0)
        :param y_offset: vertical offset (default: 0)
        :param expand: whether to fully expand instead of shrinking to fit the content (default: ``False``, *added in version 2.1.0*)
        """
        super().__init__('q-page-sticky')
        self._props['position'] = position
        self._props['offset'] = [x_offset, y_offset]
        self._props.set_bool('expand', expand)
