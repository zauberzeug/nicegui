from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import Self

from ...element import Element
from ...events import Handler, SortableEventArguments, handle_event

if TYPE_CHECKING:
    from ..mixins.sortable_element import SortableElement


class Sortable(Element, component='sortable.js', esm={'nicegui-sortable': 'dist'}):
    """Controller for SortableJS drag-and-drop sorting on a container element."""

    def __init__(
        self,
        element: SortableElement,
        options: dict[str, Any] | None,
        *,
        on_end: Handler[SortableEventArguments] | None,
        animation: float,
        handle: str | None,
        group: str | dict[str, Any] | None,
        ghost_class: str,
    ) -> None:
        super().__init__()
        self._element = element
        self._props['element-id'] = element.html_id
        self._props['options'] = {
            'animation': animation * 1000,
            'ghostClass': ghost_class,
            **({} if handle is None else {'handle': handle}),
            **({} if group is None else {'group': group}),
            **(options or {}),
        }

        self.on_end(lambda e: e.item.move(target_container=e.target, target_index=e.new_index))
        if on_end:
            self.on_end(on_end)

    def on_end(self, callback: Handler[SortableEventArguments]) -> Self:
        """Add a callback to be invoked (on the source container) when sorting ends."""
        self._element.on('sortend', lambda e: handle_event(callback, SortableEventArguments(
            sender=self._element,
            client=self._element.client,
            item=self._element.client.elements[e.args['item_id']],
            source=self._element.client.elements[e.args['from_id']],
            target=self._element.client.elements[e.args['to_id']],
            old_index=e.args['old_index'],
            new_index=e.args['new_index'],
        )), js_handler='(event) => emit(event.detail)')
        return self

    @property
    def options(self) -> dict[str, Any]:
        """The SortableJS options dictionary."""
        return self._props['options']

    @property
    def animation(self) -> float:
        """Animation duration in seconds."""
        return self._props['options'].get('animation', 150) / 1000

    @animation.setter
    def animation(self, value: float) -> None:
        self._props['options']['animation'] = value * 1000

    @property
    def handle(self) -> str | None:
        """CSS selector for drag handle elements."""
        return self._props['options'].get('handle')

    @handle.setter
    def handle(self, value: str | None) -> None:
        self._props['options']['handle'] = value

    @property
    def group(self) -> str | dict[str, Any] | None:
        """Shared group name or config dict for cross-container dragging."""
        return self._props['options'].get('group')

    @group.setter
    def group(self, value: str | dict[str, Any] | None) -> None:
        self._props['options']['group'] = value

    @property
    def ghost_class(self) -> str:
        """CSS class applied to the drop placeholder."""
        return self._props['options'].get('ghostClass', 'opacity-50')

    @ghost_class.setter
    def ghost_class(self, value: str) -> None:
        self._props['options']['ghostClass'] = value

    def enable(self) -> None:
        """Enable sorting on the container."""
        self._props['options']['disabled'] = False

    def disable(self) -> None:
        """Disable sorting on the container."""
        self._props['options']['disabled'] = True
