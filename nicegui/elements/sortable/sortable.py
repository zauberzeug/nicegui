from __future__ import annotations

import weakref
from typing import Any

from typing_extensions import Self

from nicegui.element import Element
from nicegui.events import GenericEventArguments, Handler


class Sortable(Element, component='sortable.js', esm={'nicegui-sortable': 'dist'}, default_classes='nicegui-sortable'):
    _instances: weakref.WeakValueDictionary[int, Sortable] = weakref.WeakValueDictionary()

    def __init__(
        self,
        options: dict[str, Any] | None = None, *,
        on_change: Handler[GenericEventArguments] | None = None,
        on_end: Handler[GenericEventArguments] | None = None,
        on_add: Handler[GenericEventArguments] | None = None,
        on_select: Handler[GenericEventArguments] | None = None,
        on_deselect: Handler[GenericEventArguments] | None = None,
        on_cancel_clone: Handler[GenericEventArguments] | None = None,
    ) -> None:
        """Sortable

        This element creates a draggable and sortable element based on `SortableJS <https://github.com/SortableJS/Sortable>`_.
        Child elements can be reordered by dragging.

        :param options: Dictionary of options to pass to SortableJS (see https://github.com/SortableJS/Sortable#options)
        :param on_change: Callback when the list order changes
        :param on_end: Callback when element dragging ends
        :param on_add: Callback when element is dropped into the list from another list
        :param on_select: Callback when an item is selected (MultiDrag)
        :param on_deselect: Callback when an item is deselected (MultiDrag)
        :param on_cancel_clone: Callback when an item is removed from the list into another list
        """
        super().__init__()

        self._props['options'] = {
            'animation': 150,
            'fallbackClass': 'nicegui-sortable-fallback',
            'ghostClass': 'nicegui-sortable-ghost',
            'chosenClass': 'nicegui-sortable-chosen',
            'dragClass': 'nicegui-sortable-drag',
            'swapClass': 'nicegui-sortable-swap-highlight',
            'selectedClass': 'nicegui-sortable-multi-selected',
            **(options or {}),
        }

        Sortable._instances[self.id] = self

        if on_end:
            self.on('sort_end', on_end)
        if on_add:
            self.on('sort_add', on_add)
        if on_change:
            self.on('sort_change', on_change)
        if on_cancel_clone:
            self.on('sort_cancel_clone', on_cancel_clone)
        if on_select:
            self.on('sort_select', on_select)
        if on_deselect:
            self.on('sort_deselect', on_deselect)

        self.on('sort_end', self._handle_cross_container_add)

    def on_end(self, callback: Handler[GenericEventArguments]) -> Self:
        """Add a callback to be invoked when the sorting is finished."""
        self.on('sort_end', callback)
        return self

    def on_add(self, callback: Handler[GenericEventArguments]) -> Self:
        """Add a callback to be invoked when an item is added to the sortable."""
        self.on('sort_add', callback)
        return self

    def on_change(self, callback: Handler[GenericEventArguments]) -> Self:
        """Add a callback to be invoked when the order of items changes."""
        self.on('sort_change', callback)
        return self

    def on_cancel_clone(self, callback: Handler[GenericEventArguments]) -> Self:
        """Add a callback to be invoked when cloning is canceled."""
        self.on('sort_cancel_clone', callback)
        return self

    def on_select(self, callback: Handler[GenericEventArguments]) -> Self:
        """Add a callback to be invoked when an item is selected."""
        self.on('sort_select', callback)
        return self

    def on_deselect(self, callback: Handler[GenericEventArguments]) -> Self:
        """Add a callback to be invoked when an item is deselected."""
        self.on('sort_deselect', callback)
        return self

    async def _handle_cross_container_add(self, e: GenericEventArguments) -> None:
        """Handle an element being added from another sortable container."""
        if e.args['from'] == e.args['to'] or self.props.get('cancelClone'):
            await self._synchronize_order_js_to_py()
            return

        element = next((
            child
            for child in self.default_slot.children
            if str(child.id) == e.args['item'] or child.html_id == e.args['item']
        ), None)

        sortable = next((
            instance
            for instance in Sortable._instances.values()
            if instance.default_slot.children and (str(instance.id) == e.args['to'] or instance.html_id == e.args['to'])
        ), None)

        if element and sortable:
            element.move(sortable, e.args.get('newIndex', 0))

        await self._synchronize_order_js_to_py()

    async def _synchronize_order_js_to_py(self) -> None:
        dom_order = await self.run_method('getChildrenOrder')
        if not dom_order:
            return

        id_to_item = {item.html_id: item for item in self.default_slot.children}

        ordered_items = [id_to_item[dom_id] for dom_id in dom_order if dom_id in id_to_item]
        ordered_items += [id_to_item[dom_id] for dom_id in dom_order if dom_id not in id_to_item]

        if self.default_slot.children != ordered_items:
            self.default_slot.children = ordered_items

    def set_option(self, name: str, value: Any) -> None:
        """Set a specific SortableJS option.

        :param name: Option name
        :param value: Option value
        """
        self._props['options'][name] = value
        self.run_method('setOption', name, value)

    def sort(self, order: list[Element], use_animation: bool = False) -> None:
        """Sort the elements according to the specified order.

        :param order: List of element IDs in the desired order
        :param use_animation: Whether to animate the sorting
        """
        self.default_slot.children = order
        self.run_method('sort', [item.html_id for item in order], use_animation)

    def enable(self) -> None:
        """Enable the sortable instance."""
        self.set_option('disabled', False)

    def disable(self) -> None:
        """Disable the sortable instance."""
        self.set_option('disabled', True)

    def remove_item(self, item: Element) -> None:
        """Remove an item from this sortable list.

        This removes the item both from the Python object and the DOM object.

        :param item: The element to remove.
        """
        self.run_method('remove', item.html_id)
        item.delete()

    def clear(self) -> None:
        """Remove all child elements.

        Overwritten from Element class
        """
        for slot in self.slots.values():
            for child in reversed(slot.children):
                self.remove_item(child)

    def get_child_by_id(self, html_id: str) -> Element | None:
        """Retrieve a child element by its ID within the default slot.

        :param html_id: The ID of the child element to find
        :return: The matching child Element if found, otherwise None.
        """
        return next((item for item in self.default_slot.children if item.html_id == html_id), None)

    def move_item(self, item: Element, target_index: int = -1) -> None:
        """Move an item within this sortable list and sync the DOM.

        This method ensures both Python and JavaScript stay in sync.

        :param item: The element to move
        :param target_index: The target index where to move the element
        """
        item.move(self, target_index=target_index)
        self.sort(self.default_slot.children, False)
