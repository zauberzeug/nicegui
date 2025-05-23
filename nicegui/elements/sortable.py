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

    This element creates a draggable and sortable container based on `SortableJS <https://github.com/SortableJS/Sortable>`_.

    Child elements can be reordered by dragging.
    """

    # Class-level registry to track all sortable instances
    _instances: weakref.WeakValueDictionary[int, Sortable] = weakref.WeakValueDictionary()

    def __init__(
        self,
        options: Optional[Dict] = None, *,
        on_end: Optional[Handler[GenericEventArguments]] = None,
        on_add: Optional[Handler[GenericEventArguments]] = None,
        on_sort: Optional[Handler[GenericEventArguments]] = None,
        on_move: Optional[Handler[GenericEventArguments]] = None,
        on_filter: Optional[Handler[GenericEventArguments]] = None,
        on_spill: Optional[Handler[GenericEventArguments]] = None,
        on_select: Optional[Handler[GenericEventArguments]] = None,
        on_deselect: Optional[Handler[GenericEventArguments]] = None,
    ) -> None:
        """Initialize the sortable element.

        Args:
            options: Dictionary of options to pass to SortableJS. See https://github.com/SortableJS/Sortable#options for available options.
            on_end: Callback when element dragging ends
            on_add: Callback when element is dropped into the list from another list
            on_sort: Callback when the list order changes
            on_move: Callback when you move an item
            on_filter: Callback when filtered item is clicked
            on_spill: Callback when an item is spilled outside a list
            on_select: Callback when an item is selected (MultiDrag)
            on_deselect: Callback when an item is deselected (MultiDrag)
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

        # When the order of objects have changed, synchronize
        self.on('order_updated', self._synchronize_order)

        # Add handlers for cross-container operations
        self.on('sort_add', self._handle_cross_container_add)

        # Set up event handlers
        if on_end:
            self.on('sort_end', lambda e: handle_event(on_end, e))
        if on_add:
            self.on('sort_add', lambda e: handle_event(on_add, e))
        if on_sort:
            self.on('sort_change', lambda e: handle_event(on_sort, e))
        if on_move:
            self.on('sort_move', lambda e: handle_event(on_move, e))
        if on_filter:
            self.on('sort_filter', lambda e: handle_event(on_filter, e))
        if on_spill:
            self.on('sort_spill', lambda e: handle_event(on_spill, e))
        if on_select:
            self.on('sort_select', lambda e: handle_event(on_select, e))
        if on_deselect:
            self.on('sort_deselect', lambda e: handle_event(on_deselect, e))

    def _handle_cross_container_add(self, e: GenericEventArguments) -> None:
        """Handle an element being added from another sortable container."""
        try:
            moved_dom_id = e.args.get('item')
            if not moved_dom_id:
                return

            # Extract actual element ID (remove 'c' prefix if present)
            moved_id = moved_dom_id[1:] if moved_dom_id.startswith('c') else moved_dom_id

            # Get the index where the item should be inserted
            new_index = e.args.get('newIndex', 0)

            # Search all other sortable instances for the element
            found_element = None
            source_sortable = None

            for instance in Sortable._instances.values():
                if instance == self:
                    continue

                if instance.default_slot and instance.default_slot.children:
                    for child in instance.default_slot.children:
                        if str(child.id) == moved_id:
                            found_element = child
                            source_sortable = instance
                            break

            if found_element and source_sortable:
                # Remove the element from the source sortable
                if found_element in source_sortable.default_slot.children:
                    source_sortable.default_slot.children.remove(found_element)

                # Add the element to this sortable at the specified index
                if found_element not in self.default_slot.children:
                    if new_index < len(self.default_slot.children):
                        self.default_slot.children.insert(new_index, found_element)
                    else:
                        self.default_slot.children.append(found_element)
        except Exception as err:
            print(f'Error handling cross-container add: {err}')

    def _synchronize_order(self, e: GenericEventArguments) -> None:
        """Synchronize the Python-side order with the JavaScript DOM order."""
        try:
            if not self.default_slot:
                return

            # Check if this is a regular order update with childrenData
            if e.args.get('childrenData') is not None:
                ordered_items: list[Element] = []

                # First, create a map of ID to item
                # Add "c" in front of ID to match DOMs ID
                id_to_item = {f'c{item.id}': item for item in self.default_slot.children}

                # Then construct the new order based on the DOM order
                for item in e.args.get('childrenData'):
                    if item['id'] in id_to_item:
                        ordered_items.append(id_to_item[item['id']])

                # Add any remaining items that might not be in the currentOrder
                for item in self.default_slot.children:
                    if f'c{item.id}' not in [child['id'] for child in e.args.get('childrenData')] and item not in ordered_items:
                        ordered_items.append(item)

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
