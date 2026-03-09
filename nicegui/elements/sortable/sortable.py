from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import Self

from ... import core, json
from ...events import Handler, SortableEventArguments, handle_event
from ...observables import ObservableDict

if TYPE_CHECKING:
    from ..mixins.sortable_element import SortableElement


class Sortable:
    """Controller for SortableJS drag-and-drop sorting on a container element."""

    def __init__(
        self,
        element: SortableElement,
        options: dict[str, Any] | None = None,
        *,
        on_end: Handler[SortableEventArguments] | None = None,
        animation: float = 0.15,
        handle: str | None = None,
        group: str | dict[str, Any] | None = None,
        ghost_class: str = 'opacity-50',
    ) -> None:
        self._element = element

        self._options = ObservableDict({
            'animation': animation * 1000,
            'ghostClass': ghost_class,
            **({} if handle is None else {'handle': handle}),
            **({} if group is None else {'group': group}),
            **(options or {}),
        }, on_change=lambda: self._element.client.run_javascript(';'.join(
            f'{self._element.html_id}._sortable.option({json.dumps(k)}, {json.dumps(v)})'
            for k, v in self._options.items()
        )))

        self.on_end(lambda e: e.item.move(target_container=e.target, target_index=e.new_index))
        if on_end:
            self.on_end(on_end)

        if not core.loop:
            return  # this must be a script mode preflight run, so we skip initializing the SortableJS instance
        element.client.run_javascript(f'''
            (async () => {{
                const {{ Sortable }} = await import('nicegui-sortable');
                const sortable = Sortable.create({element.html_id}, {{
                    ...{json.dumps(self._options)},
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

    @property
    def options(self) -> ObservableDict:
        """The SortableJS options dictionary."""
        return self._options

    @property
    def animation(self) -> float:
        """Animation duration in seconds."""
        return self._options.get('animation', 150) / 1000

    @animation.setter
    def animation(self, value: float) -> None:
        self._options['animation'] = value * 1000

    @property
    def handle(self) -> str | None:
        """CSS selector for drag handle elements."""
        return self._options.get('handle')

    @handle.setter
    def handle(self, value: str | None) -> None:
        self._options['handle'] = value

    @property
    def group(self) -> str | dict[str, Any] | None:
        """Shared group name or config dict for cross-container dragging."""
        return self._options.get('group')

    @group.setter
    def group(self, value: str | dict[str, Any] | None) -> None:
        self._options['group'] = value

    @property
    def ghost_class(self) -> str:
        """CSS class applied to the drop placeholder."""
        return self._options.get('ghostClass', 'opacity-50')

    @ghost_class.setter
    def ghost_class(self, value: str) -> None:
        self._options['ghostClass'] = value

    def enable(self) -> None:
        """Enable sorting on the container."""
        self._options['disabled'] = False

    def disable(self) -> None:
        """Disable sorting on the container."""
        self._options['disabled'] = True
