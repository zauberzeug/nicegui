from typing import Literal, Optional

from ..element import Element


class Column(Element):

    def __init__(self, *,
                 wrap: bool = False,
                 align_items: Optional[Literal['start', 'end', 'center', 'baseline', 'stretch']] = None,
                 ) -> None:
        """Column Element

        Provides a container which arranges its child in a column.

        :param wrap: whether to wrap the content (default: `False`)
        :param align_items: alignment of the items in the column (default: `None`)
        """
        super().__init__('div')
        self._classes.append('nicegui-column')
        if align_items:
            self._classes.append(f'items-{align_items}')

        if wrap:
            self._style['flex-wrap'] = 'wrap'
