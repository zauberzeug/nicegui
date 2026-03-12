from typing import Literal

from ..element import Element


class Column(Element, default_classes='nicegui-column'):

    def __init__(self, *,
                 wrap: bool = False,
                 align_items: Literal['start', 'end', 'center', 'baseline', 'stretch'] | None = None,
                 ) -> None:
        """Column Element

        Provides a container which arranges its child in a column.

        :param wrap: whether to wrap the content (default: `False`)
        :param align_items: alignment of the items in the column ("start", "end", "center", "baseline", or "stretch"; default: `None`)
        """
        super().__init__('div')
        if align_items:
            self._classes.append(f'items-{align_items}')

        if wrap:
            self._style['flex-wrap'] = 'wrap'
