from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...element import Element

if TYPE_CHECKING:
    from ...events import Handler, SortableEventArguments
    from ..sortable import Sortable


class SortableElement(Element):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._sortable: Sortable | None = None

    def make_sortable(
        self,
        options: dict[str, Any] | None = None,
        *,
        on_end: Handler[SortableEventArguments] | None = None,
        animation: float = 0.15,
        handle: str | None = None,
        group: str | dict[str, Any] | None = None,
        ghost_class: str = 'opacity-50',
    ) -> Sortable:
        """Make this container sortable via drag-and-drop using SortableJS.

        Returns a ``Sortable`` controller that can be used to enable/disable sorting
        and change options.

        Note: Setting a custom HTML ID on the container (e.g. via ``.props('id="my-list"')``) is not supported
        and will break the internal slot synchronization.

        *Added in version 3.11.0*

        :param options: dictionary of raw SortableJS options (overrides named params like ``animation`` if both are given)
        :param on_end: callback invoked when a sort operation ends (fires on the source container only, even for cross-container moves)
        :param animation: animation duration in seconds (default: 0.15)
        :param handle: CSS selector for drag handle elements (default: ``None``, entire item is draggable)
        :param group: shared group name or config dict for cross-container dragging
        :param ghost_class: CSS class applied to the drop placeholder (default: "opacity-50")
        """
        from ..sortable import Sortable  # pylint: disable=import-outside-toplevel
        if self._sortable is not None:
            raise RuntimeError('This element is already sortable.')
        with self.client.layout:
            self._sortable = Sortable(
                self,
                options,
                on_end=on_end,
                animation=animation,
                handle=handle,
                group=group,
                ghost_class=ghost_class,
            )
        return self._sortable

    def _handle_delete(self) -> None:
        super()._handle_delete()
        if self._sortable is not None:
            if self._sortable.parent_slot is not None and self._sortable in self._sortable.parent_slot.children:
                self._sortable.delete()
            self._sortable = None
