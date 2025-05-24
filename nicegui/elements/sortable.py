from __future__ import annotations

import weakref
from typing import Any, Dict, List, Optional

from nicegui.element import Element
from nicegui.events import GenericEventArguments, Handler, handle_event


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
        options: Optional[Dict] = None, *,
        on_choose: Optional[Handler[GenericEventArguments]] = None,
        on_unchoose: Optional[Handler[GenericEventArguments]] = None,
        on_start: Optional[Handler[GenericEventArguments]] = None,
        on_end: Optional[Handler[GenericEventArguments]] = None,
        on_add: Optional[Handler[GenericEventArguments]] = None,
        on_update: Optional[Handler[GenericEventArguments]] = None,
        on_sort: Optional[Handler[GenericEventArguments]] = None,
        on_remove: Optional[Handler[GenericEventArguments]] = None,
        on_move: Optional[Handler[GenericEventArguments]] = None,
        on_clone: Optional[Handler[GenericEventArguments]] = None,
        on_change: Optional[Handler[GenericEventArguments]] = None,
        on_filter: Optional[Handler[GenericEventArguments]] = None,
        on_spill: Optional[Handler[GenericEventArguments]] = None,
        on_select: Optional[Handler[GenericEventArguments]] = None,
        on_deselect: Optional[Handler[GenericEventArguments]] = None,
        on_remove_on_add: Optional[Handler[GenericEventArguments]] = None,
    ) -> None:
        """Initialize the sortable element.

        Args:
            options: Dictionary of options to pass to SortableJS. See https://github.com/SortableJS/Sortable#options for available options.
            on_choose: Callback when element is chosen
            on_unchoose: Callback when element is unchosen
            on_start: Callback when element dragging starts
            on_end: Callback when element dragging ends
            on_add: Callback when element is dropped into the list from another list
            on_update: Callback when sorting within list is changed
            on_sort: Called by any change to the list (add / update / remove)
            on_remove: Callback when element is removed from the list into another list
            on_move: Callback when you move an item
            on_clone: Callback when creating a clone of element
            on_change: Callback when dragging element changes position
            on_filter: Callback when filtered item is clicked
            on_spill: Callback when an item is spilled outside a list
            on_select: Callback when an item is selected (MultiDrag)
            on_deselect: Callback when an item is deselected (MultiDrag)
            on_remove_on_add: Callback when an item is removed from the list into another list
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

        # Add handlers for cross-element operations
        self.on('sort_end', self._handle_cross_element_add)

        # Set up event handlers
        if on_choose:
            self.on('sort_choose', lambda e: handle_event(on_choose, e))
        if on_unchoose:
            self.on('sort_unchoose', lambda e: handle_event(on_unchoose, e))
        if on_start:
            self.on('sort_start', lambda e: handle_event(on_start, e))
        if on_end:
            self.on('sort_end', lambda e: handle_event(on_end, e))
        if on_add:
            self.on('sort_add', lambda e: handle_event(on_add, e))
        if on_update:
            self.on('sort_update', lambda e: handle_event(on_update, e))
        if on_sort:
            self.on('sort_sort', lambda e: handle_event(on_sort, e))
        if on_remove:
            self.on('sort_remove', lambda e: handle_event(on_remove, e))
        if on_move:
            self.on('sort_move', lambda e: handle_event(on_move, e))
        if on_clone:
            self.on('sort_clone', lambda e: handle_event(on_clone, e))
        if on_change:
            self.on('sort_change', lambda e: handle_event(on_change, e))
        if on_filter:
            self.on('sort_filter', lambda e: handle_event(on_filter, e))
        if on_spill:
            self.on('sort_spill', lambda e: handle_event(on_spill, e))
        if on_select:
            self.on('sort_select', lambda e: handle_event(on_select, e))
        if on_deselect:
            self.on('sort_deselect', lambda e: handle_event(on_deselect, e))
        if on_remove_on_add:
            self.on('sort_remove_on_add', lambda e: handle_event(on_remove_on_add, e))

    async def _handle_cross_element_add(self, e: GenericEventArguments) -> None:
        """Handle when an element being moved from another sortable element."""
        try:

            # If moved within its own list, ignore
            if e.args['from'] == e.args['to'] or self.props.get('removeOnAdd', False):
                await self._synchronize_order_js_to_py()
                return

            moved_dom_id = e.args.get('item')

            # Extract actual element ID (remove 'c' prefix if present)
            moved_id = moved_dom_id[1:] if moved_dom_id.startswith('c') else moved_dom_id

            # Get the index where the item should be inserted
            new_index = e.args.get('newIndex', 0)

            # Search all other sortable instances for the element
            found_element = None

            for instance in Sortable._instances.values():
                if instance == self:
                    continue

                if instance.default_slot and instance.default_slot.children:
                    for child in instance.default_slot.children:
                        if str(child.id) == moved_id:
                            found_element = child
                            break

            if found_element:
                found_element.move(self, new_index)

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

        Args:
            name: Option name
            value: Option value
        """
        self._props['options'][name] = value
        self.run_method('setOption', name, value)

    def get_option(self, name: str) -> Any:
        """Get a specific SortableJS option.

        Args:
            name: Option name

        Returns:
            The current value of the option
        """
        return self._props['options'].get(name)

    def sort(self, order: List[Element], use_animation: bool = False) -> None:
        """Sort the elements according to the specified order.

        Args:
            order: List of element IDs in the desired order
            use_animation: Whether to animate the sorting
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

    # MultiDrag plugin methods
    async def get_selected(self) -> List[str]:
        """Get the currently selected items when using MultiDrag.

        Returns:
            A list of selected element IDs
        """
        return await self.run_method('getSelected')

    def select(self, element_id: str) -> None:
        """Select an item programmatically when using MultiDrag.

        Args:
            element_id: ID of the element to select
        """
        self.run_method('select', element_id)

    def deselect(self, element_id: str) -> None:
        """Deselect an item programmatically when using MultiDrag.

        Args:
            element_id: ID of the element to deselect
        """
        self.run_method('deselect', element_id)

    def remove_item(self, item: Element | int | str) -> None:
        """Remove an item from this sortable list.

        This removes the item both from the Python object and the DOM object.

        Args:
            item: The element to remove. Can be:
                - An Element object
                - A string ID (with or without 'c' prefix)
                - An integer ID
        """
        # Get the element and its DOM ID
        element_to_remove = None
        dom_id = None

        # Handle different item types
        if isinstance(item, Element):
            element_to_remove = item
            dom_id = f'c{item.id}'
        elif isinstance(item, str):
            dom_id = item if item.startswith('c') else f'c{item}'

            # Try to find the element in our children
            if self.default_slot and self.default_slot.children:
                # Get the ID without the 'c' prefix
                raw_id = dom_id[1:] if dom_id.startswith('c') else dom_id
                for child in self.default_slot.children:
                    if str(child.id) == raw_id:
                        element_to_remove = child
                        break
        elif isinstance(item, int):
            dom_id = f'c{item}'

            # Try to find the element in our children
            if self.default_slot and self.default_slot.children:
                for child in self.default_slot.children:
                    if child.id == item:
                        element_to_remove = child
                        break
        else:
            raise TypeError(f'Expected Element, str, or int, got {type(item).__name__}')

        # Remove from DOM
        self.run_method('remove', dom_id)

        # Remove from Python data structure and delete the element
        if element_to_remove:
            # Remove from parent slot's children list if present
            if self.default_slot and element_to_remove in self.default_slot.children:
                self.default_slot.children.remove(element_to_remove)

            # Delete the element
            element_to_remove.delete()

    def clear(self) -> None:
        """Remove all child elements.

        Overwritten from Element class
        """
        for slot in self.slots.values():
            for child in reversed(slot.children):
                self.remove_item(child)

    def get_child_by_id(self, item_id: str | int) -> Element | None:
        """Retrieve a child element by its ID within the default slot.

        Args:
            item_id: The ID of the child element to find, with optional 'c' prefix.

        Returns:
            The matching child Element if found, otherwise None.
        """
        id_number = int(str(item_id)[1:] if str(item_id).startswith('c') else item_id)
        for item in self.default_slot.children:
            if item.id == id_number:
                return item

        return None

    def move_item(self, item: Element, target_index: int = -1) -> None:
        """Move an item within this sortable list and sync the DOM.

        This method ensures both Python and JavaScript stay in sync.

        Args:
            item: The element to move
            target_index: The target index where to move the element
        """
        # First perform the standard move operation in Python
        item.move(self, target_index=target_index)

        # Then synchronize the DOM to match the Python order
        self.sort(self.default_slot.children, False)
