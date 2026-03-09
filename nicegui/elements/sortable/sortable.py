from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import Self

from ... import core, json
from ...events import Handler, SortableEventArguments, handle_event

if TYPE_CHECKING:
    from ...element import Element


class Sortable:
    """Controller for SortableJS drag-and-drop sorting on a container element."""

    def __init__(
        self,
        element: Element,
        options: dict[str, Any] | None = None,
        *,
        on_end: Handler[SortableEventArguments] | None = None,
        animation: float = 0.15,
        handle: str | None = None,
        group: str | dict[str, Any] | None = None,
        ghost_class: str = 'opacity-50',
    ) -> None:
        self._element = element

        self.on_end(lambda e: e.item.move(target_container=e.target, target_index=e.new_index))
        if on_end:
            self.on_end(on_end)

        if not core.loop:
            return  # this must be a script mode preflight run, so we skip initializing the SortableJS instance
        element.client.run_javascript(f'''
            (async () => {{
                const {{ Sortable }} = await import('nicegui-sortable');
                const sortable = Sortable.create({element.html_id}, {{
                    animation: {animation * 1000},
                    ghostClass: {json.dumps(ghost_class)},
                    handle: {json.dumps(handle)},
                    group: {json.dumps(group)},
                    ...{json.dumps(options or {})},
                    onEnd: (evt) => {{
                        // sync client-side element tree to prevent snap-back on next server update
                        const fromId = parseInt(evt.from.id.substring(1));
                        const toId = parseInt(evt.to.id.substring(1));
                        const fromSlot = window.mounted_app?.elements?.[fromId]?.slots?.default;
                        const toSlot = window.mounted_app?.elements?.[toId]?.slots?.default;
                        if (fromSlot && fromSlot.ids) {{
                            const itemId = fromSlot.ids.splice(evt.oldIndex, 1)[0];
                            if (fromId === toId) {{
                                fromSlot.ids.splice(evt.newIndex, 0, itemId);
                            }} else if (toSlot && toSlot.ids) {{
                                toSlot.ids.splice(evt.newIndex, 0, itemId);
                            }}
                        }}
                        {element.html_id}.dispatchEvent(new CustomEvent('sortend', {{
                            detail: {{
                                item_id: parseInt(evt.item.id.substring(1)),
                                from_id: fromId,
                                to_id: toId,
                                old_index: evt.oldIndex,
                                new_index: evt.newIndex,
                            }},
                            bubbles: false,
                        }}));
                    }},
                }});
                {element.html_id}._sortable = sortable;
            }})()
        ''')

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

    def enable(self) -> None:
        """Enable sorting on the container."""
        self.set_option('disabled', False)

    def disable(self) -> None:
        """Disable sorting on the container."""
        self.set_option('disabled', True)

    def set_option(self, key: str, value: Any) -> None:
        """Set a SortableJS option."""
        self._element.client.run_javascript(f'''
            {self._element.html_id}._sortable.option({json.dumps(key)}, {json.dumps(value)})
        ''')
