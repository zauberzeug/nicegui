from typing import Literal, Optional

from ..element import Element


class Row(Element):

    def __init__(self, *,
                 wrap: bool = True,
                 align_items: Optional[Literal['start', 'end', 'center', 'baseline', 'stretch']] = None,
                 ) -> None:
        """Row Element

        Provides a container which arranges its child in a row.

        :param wrap: whether to wrap the content (default: `True`)
        :param align_items: alignment of the items in the row (default: `None`)
        """
        super().__init__('div')
        self._classes.append('nicegui-row')
        self._classes.append('row')  # NOTE: for compatibility with Quasar's col-* classes
        if align_items:
            self._classes.append(f'items-{align_items}')

        if not wrap:
            self._style['flex-wrap'] = 'nowrap'
