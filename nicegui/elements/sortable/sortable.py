from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from typing_extensions import Self

from ... import core
from ...events import Handler, SortableEventArguments, handle_event

if TYPE_CHECKING:
    from ...element import Element

_SORTEND_ARGS = ['item_id', 'from_id', 'to_id', 'old_index', 'new_index']
_JS_HANDLER = '(event) => emit(event.detail)'

_INIT_JS = '''
(async () => {{
    const {{ Sortable }} = await import('nicegui-sortable');
    const el = document.getElementById('c' + {element_id});
    if (!el) return;
    const sortable = Sortable.create(el, {{
        {options}
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
            el.dispatchEvent(new CustomEvent('sortend', {{
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
    el._nicegui_sortable = sortable;
}})()
'''


def _build_options(options: dict[str, Any]) -> str:
    parts = []
    for key, value in options.items():
        parts.append(f'{key}: {json.dumps(value)},')
    return '\n        '.join(parts)


class Sortable:
    """Controller for SortableJS drag-and-drop sorting on a container element.

    SortableJS fires ``onEnd`` on the *source* container only — even for cross-container moves,
    only the source container's ``on_end`` callbacks are invoked.
    """

    def __init__(
        self,
        element: Element,
        options: dict[str, Any] | None = None,
        *,
        on_end: Handler[SortableEventArguments] | None = None,
        animation: int = 150,
        handle: str | None = None,
        group: str | dict[str, Any] | None = None,
        filter: str | None = None,  # pylint: disable=redefined-builtin
        ghost_class: str = 'opacity-50',
    ) -> None:
        self._element = element

        element.on('sortend', self._handle_sort_end, _SORTEND_ARGS, js_handler=_JS_HANDLER)

        if on_end:
            self.on_end(on_end)

        merged: dict[str, Any] = {}
        if options:
            merged.update(options)
        merged.setdefault('animation', animation)
        if handle is not None:
            merged.setdefault('handle', handle)
        if group is not None:
            merged.setdefault('group', group)
        if filter is not None:
            merged.setdefault('filter', filter)
        merged.setdefault('ghostClass', ghost_class)

        js = _INIT_JS.format(element_id=element.id, options=_build_options(merged))

        if core.loop:
            element.client.run_javascript(js)
        else:
            element.client.on_connect(lambda: element.client.run_javascript(js))

    def on_end(self, callback: Handler[SortableEventArguments]) -> Self:
        """Add a callback to be invoked when sorting ends.

        Note: For cross-container moves, only the *source* container's callbacks fire.

        :param callback: callback that receives SortableEventArguments
        """
        self._element.on('sortend', lambda e: self._fire_user_handler(callback, e),
                         _SORTEND_ARGS, js_handler=_JS_HANDLER)
        return self

    def enable(self) -> None:
        """Enable sorting on the container."""
        self._run_sortable_js('option("disabled", false)')

    def disable(self) -> None:
        """Disable sorting on the container."""
        self._run_sortable_js('option("disabled", true)')

    def set_option(self, key: str, value: Any) -> None:
        """Set a SortableJS option.

        :param key: option name
        :param value: option value
        """
        self._run_sortable_js(f'option({json.dumps(key)}, {json.dumps(value)})')

    def destroy(self) -> None:
        """Destroy the SortableJS instance and clean up."""
        el_js = f'document.getElementById("c{self._element.id}")'
        self._element.client.run_javascript(
            f'const s = {el_js}._nicegui_sortable; '
            f'if (s) {{ s.destroy(); {el_js}._nicegui_sortable = null; }}'
        )

    def _run_sortable_js(self, method_call: str) -> None:
        self._element.client.run_javascript(
            f'document.getElementById("c{self._element.id}")._nicegui_sortable.{method_call}'
        )

    def _handle_sort_end(self, e: Any) -> None:
        """Sync the server-side element tree to match the client after a drag operation."""
        args = e.args
        item_id = args['item_id']
        from_id = args['from_id']
        to_id = args['to_id']
        old_index = args['old_index']
        new_index = args['new_index']

        client = self._element.client
        item = client.elements.get(item_id)
        if item is None:
            return

        if from_id == to_id:
            parent_slot = item.parent_slot
            if parent_slot is None:
                return
            children = parent_slot.children
            if old_index < len(children):
                child = children.pop(old_index)
                children.insert(new_index, child)
        else:
            target = client.elements.get(to_id)
            if target is None:
                return
            item.move(target_container=target, target_index=new_index)

    def _fire_user_handler(self, callback: Handler[SortableEventArguments], e: Any) -> None:
        args = e.args
        client = self._element.client
        item = client.elements.get(args['item_id'])
        source = client.elements.get(args['from_id'])
        target = client.elements.get(args['to_id'])
        if item is None or source is None or target is None:
            return
        handle_event(callback, SortableEventArguments(
            sender=self._element,
            client=client,
            old_index=args['old_index'],
            new_index=args['new_index'],
            item=item,
            source=source,
            target=target,
        ))
