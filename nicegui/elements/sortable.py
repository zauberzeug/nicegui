from __future__ import annotations

import weakref
from typing import Any

from typing_extensions import Self

from nicegui.element import Element
from nicegui.events import EventT, GenericEventArguments, Handler, handle_event


class Sortable(Element,
               component='sortable.js',
               dependencies=['lib/sortable/sortable.complete.esm.js'],
               default_classes='nicegui-sortable'):
    """Sortable.

    This element creates a draggable and sortable element based on `SortableJS <https://github.com/SortableJS/Sortable>`_.

    Child elements can be reordered by dragging.
    """

    # Class-level registry to track all sortable instances
    _instances: weakref.WeakValueDictionary[int, Sortable] = weakref.WeakValueDictionary()

    def __init__(
        self,
        options: dict[str, Any] | None = None, *,
        on_change: Handler[GenericEventArguments] | None = None,
        on_end: Handler[GenericEventArguments] | None = None,
        on_add: Handler[GenericEventArguments] | None = None,
        on_filter: Handler[GenericEventArguments] | None = None,
        on_spill: Handler[GenericEventArguments] | None = None,
        on_select: Handler[GenericEventArguments] | None = None,
        on_deselect: Handler[GenericEventArguments] | None = None,
        on_cancel_clone: Handler[GenericEventArguments] | None = None,
    ) -> None:
        """Initialize the sortable element.

        :param options: Dictionary of options to pass to SortableJS. See https://github.com/SortableJS/Sortable#options for available options.
        :param on_change: Callback when the list order changes
        :param on_end: Callback when element dragging ends
        :param on_add: Callback when element is dropped into the list from another list
        :param on_move: Callback when you move an item
        :param on_filter: Callback when filtered item is clicked
        :param on_spill: Callback when an item is spilled outside a list
        :param on_select: Callback when an item is selected (MultiDrag)
        :param on_deselect: Callback when an item is deselected (MultiDrag)
        :param on_cancel_clone: Callback when an item is removed from the list into another list
        """
        super().__init__()

        # Initialize options with defaults if not provided
        options = options or {}

        # Set up SortableJS options
        sortable_options = {
            # Common defaults
            'animation': 150,
            'fallbackClass': 'nicegui-sortable-fallback',
            'ghostClass': 'nicegui-sortable-ghost',
            'chosenClass': 'nicegui-sortable-chosen',
            'dragClass': 'nicegui-sortable-drag',
            'swapClass': 'nicegui-sortable-swap-highlight',
            'selectedClass': 'nicegui-sortable-multi-selected',
            **options
        }
        self._props['options'] = sortable_options

        # Register this instance in the class registry
        Sortable._instances[self.id] = self

        self._end_handlers = [on_end] if on_end else []
        self._add_handlers = [on_add] if on_add else []
        self._change_handlers = [on_change] if on_change else []
        self._cancel_clone_handlers = [on_cancel_clone] if on_cancel_clone else []
        self._filter_handlers = [on_filter] if on_filter else []
        self._spill_handlers = [on_spill] if on_spill else []
        self._select_handlers = [on_select] if on_select else []
        self._deselect_handlers = [on_deselect] if on_deselect else []

        # Set up event handling wrapper function
        def handle_sortable_event(event_handlers: list[Handler[EventT]], e: EventT):
            for handler in event_handlers:
                handle_event(handler, e)

        # Register event handlers
        self.on('sort_end', lambda e: handle_sortable_event(self._end_handlers, e))
        self.on('sort_add', lambda e: handle_sortable_event(self._add_handlers, e))
        self.on('sort_change', lambda e: handle_sortable_event(self._change_handlers, e))
        self.on('sort_cancel_clone', lambda e: handle_sortable_event(self._cancel_clone_handlers, e))
        self.on('sort_filter', lambda e: handle_sortable_event(self._filter_handlers, e))
        self.on('sort_spill', lambda e: handle_sortable_event(self._spill_handlers, e))
        self.on('sort_select', lambda e: handle_sortable_event(self._select_handlers, e))
        self.on('sort_deselect', lambda e: handle_sortable_event(self._deselect_handlers, e))

        # Add handlers for cross-element operations
        self.on('sort_end', self._handle_cross_container_add)

    def on_end(self, callback: Handler[GenericEventArguments]) -> Self:
        """ Add a callback to be invoked when the sorting is finished."""
        self._end_handlers.append(callback)
        return self

    def on_add(self, callback: Handler[GenericEventArguments]) -> Self:
        """ Add a callback to be invoked when an item is added to the sortable."""
        self._add_handlers.append(callback)
        return self

    def on_change(self, callback: Handler[GenericEventArguments]) -> Self:
        """ Add a callback to be invoked when the order of items changes."""
        self._change_handlers.append(callback)
        return self

    def on_cancel_clone(self, callback: Handler[GenericEventArguments]) -> Self:
        """ Add a callback to be invoked when cloning is canceled."""
        self._cancel_clone_handlers.append(callback)
        return self

    def on_filter(self, callback: Handler[GenericEventArguments]) -> Self:
        """ Add a callback to be invoked when the sortable is filtered."""
        self._filter_handlers.append(callback)
        return self

    def on_spill(self, callback: Handler[GenericEventArguments]) -> Self:
        """ Add a callback to be invoked when an item spills out of the sortable."""
        self._spill_handlers.append(callback)
        return self

    def on_select(self, callback: Handler[GenericEventArguments]) -> Self:
        """ Add a callback to be invoked when an item is selected."""
        self._select_handlers.append(callback)
        return self

    def on_deselect(self, callback: Handler[GenericEventArguments]) -> Self:
        """ Add a callback to be invoked when an item is deselected."""
        self._deselect_handlers.append(callback)
        return self

    async def _handle_cross_container_add(self, e: GenericEventArguments) -> None:
        """Handle an element being added from another sortable container."""
        try:

            # If moved within its own list, ignore
            if e.args['from'] == e.args['to'] or self.props.get('cancelClone', False):
                await self._synchronize_order_js_to_py()
                return

            # Search all other sortable instances for the element
            element = None
            to_instance = None

            # Find the to-instance and the moved element
            for instance in Sortable._instances.values():
                if instance == self:
                    for child in self.default_slot.children:
                        if str(child.id) == e.args['item'] or child.html_id == e.args['item']:
                            element = child
                            continue

                if instance.default_slot and instance.default_slot.children:
                    if str(instance.id) == e.args['to'] or instance.html_id == e.args['to']:
                        to_instance = instance

            if element and to_instance:
                element.move(to_instance, e.args.get('newIndex', 0))

        except Exception as err:
            print(f'Error handling cross-element add: {err}')

        await self._synchronize_order_js_to_py()

    async def _synchronize_order_js_to_py(self) -> None:
        """Synchronize the Python-side order with the JavaScript DOM order."""
        try:

            if not self.default_slot:
                return

            # Get the current DOM order directly from JavaScript
            dom_order = await self.run_method('getChildrenOrder')

            if not dom_order:
                return

            # Create a map of DOM ID to Python object
            id_to_item = {f'c{item.id}': item for item in self.default_slot.children}

            # Create a new ordered list based on the DOM order
            ordered_items: list[Element] = []
            ordered_items_id: list[str] = []

            # First, add items in the order they appear in the DOM
            for dom_id in dom_order:
                if dom_id in id_to_item:
                    ordered_items.append(id_to_item[dom_id])
                    ordered_items_id.append(dom_id)

            # Then add any remaining items that might not be in the DOM
            for item in self.default_slot.children:
                item_dom_id = f'c{item.id}'
                if item_dom_id not in dom_order and item not in ordered_items:
                    ordered_items.append(item)
                    ordered_items_id.append(item_dom_id)

            # Only update if the order has actually changed
            if ordered_items != self.default_slot.children:
                # Replace the children with the ordered list
                self.default_slot.children = ordered_items

        except Exception as err:
            print(f'Error synchronizing order: {err}')

    def set_option(self, name: str, value: Any) -> None:
        """Set a specific SortableJS option.

        :param name: Option name
        :param value: Option value
        """
        self._props['options'][name] = value
        self.run_method('setOption', name, value)

    def get_option(self, name: str) -> Any:
        """Get a specific SortableJS option.

        :param name: Option name

        Returns:
            The current value of the option
        """
        return self._props['options'].get(name)

    def sort(self, order: list[Element], use_animation: bool = False) -> None:
        """Sort the elements according to the specified order.

        :param order: List of element IDs in the desired order
        :param use_animation: Whether to animate the sorting
        """
        self.default_slot.children = order
        # Add "c" in front of ID to match DOMs ID
        self.run_method('sort', [f'c{item.id}' for item in order], use_animation)

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
        # Remove from DOM
        self.run_method('remove', item.html_id)

        # Remove from Python data structure and delete the element
        if item:
            # Remove from parent slot's children list if present
            if self.default_slot and item in self.default_slot.children:
                self.default_slot.children.remove(item)

            # Delete the element
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

        Returns:
            The matching child Element if found, otherwise None.
        """
        for item in self.default_slot.children:
            if item.html_id == html_id:
                return item

        return None

    def move_item(self, item: Element, target_index: int = -1) -> None:
        """Move an item within this sortable list and sync the DOM.

        This method ensures both Python and JavaScript stay in sync.

        :param item: The element to move
        :param target_index: The target index where to move the element
        """
        # First perform the standard move operation in Python
        item.move(self, target_index=target_index)

        # Then synchronize the DOM to match the Python order
        self.sort(self.default_slot.children, False)

    # MultiDrag plugin methods
    def select(self, element_id: str) -> None:
        """Select an item programmatically when using MultiDrag.

        :param element_id: HTML ID of the element to select
        """
        self.run_method('select', element_id)

    def deselect(self, element_id: str) -> None:
        """Deselect an item programmatically when using MultiDrag.

        :param element_id: HTML ID of the element to deselect
        """
        self.run_method('deselect', element_id)
