from __future__ import annotations

from typing import Literal

from ..element import Element
from ..helpers import DEFAULT_CLASS, DEFAULT_STYLE


class Column(Element, default_classes='nicegui-column'):

    def __init__(self, *,
                 wrap: bool = DEFAULT_STYLE or False,  # type: ignore[assignment]
                 align_items: Literal[
                     'start',
                     'end',
                     'center',
                     'baseline',
                     'stretch',
                 ] | None = DEFAULT_CLASS or None,  # type: ignore[assignment]
                 ) -> None:
        """Column Element

        Provides a container which arranges its child in a column.

        :param wrap: whether to wrap the content (default: ``False`` unless overridden by default style)
        :param align_items: alignment of the items in the column ("start", "end", "center", "baseline", or "stretch"; default: ``None`` unless overridden by default class)
        """
        super().__init__('div')
        if align_items is None:
            self._classes[:] = set(self._default_classes) - \
                {'items-start', 'items-end', 'items-center', 'items-baseline', 'items-stretch'}
        elif isinstance(align_items, str):
            self._classes.append(f'items-{align_items}')

        if wrap is False:
            self._style['flex-wrap'] = 'nowrap'
        elif wrap is True:
            self._style['flex-wrap'] = 'wrap'
