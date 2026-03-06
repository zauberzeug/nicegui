from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...element import Element

if TYPE_CHECKING:
    from ...events import Handler, SortableEventArguments
    from ..sortable import Sortable


class SortableElement(Element):

    def make_sortable(
        self: Element,
        options: dict[str, Any] | None = None,
        *,
        on_end: Handler[SortableEventArguments] | None = None,
        animation: int = 150,
        handle: str | None = None,
        group: str | dict[str, Any] | None = None,
        filter: str | None = None,  # pylint: disable=redefined-builtin
        ghost_class: str = 'opacity-50',
    ) -> Sortable:
        """Make this container sortable via drag-and-drop using SortableJS.

        Returns a ``Sortable`` controller that can be used to enable/disable sorting,
        change options, or destroy the SortableJS instance.

        :param options: dictionary of raw SortableJS options (merged with named params)
        :param on_end: callback invoked when a sort operation ends (fires on the source container only, even for cross-container moves)
        :param animation: animation speed in ms (default: 150)
        :param handle: CSS selector for drag handle elements (default: ``None``, entire item is draggable)
        :param group: shared group name or config dict for cross-container dragging
        :param filter: CSS selector for elements that should not be draggable
        :param ghost_class: CSS class applied to the drop placeholder (default: ``'opacity-50'``)
        """
        from ..sortable import Sortable  # pylint: disable=import-outside-toplevel
        return Sortable(
            self,
            options,
            on_end=on_end,
            animation=animation,
            handle=handle,
            group=group,
            filter=filter,
            ghost_class=ghost_class,
        )
