from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

from nicegui.element import Element
from nicegui.events import handle_event


class Sortable(Element,
               component='sortable.js',
               dependencies=[],
               default_classes='nicegui-sortable'):
    """SortableJS integration for NiceGUI.

    This element creates a draggable and sortable container. Child elements can be reordered by dragging.
    """

    def __init__(
        self,
        options: Optional[Dict] = None, *,  # Make options optional with default None
        on_end: Optional[Callable] = None,
        on_add: Optional[Callable] = None,
        on_sort: Optional[Callable] = None,
        on_move: Optional[Callable] = None,
        on_filter: Optional[Callable] = None,
        on_spill: Optional[Callable] = None,
        on_select: Optional[Callable] = None,
        on_deselect: Optional[Callable] = None,
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

        # Add the resource
        self.add_resource(Path(__file__).parent / 'lib' / 'sortable')

        # Apply flex layout by default
        self.classes('nicegui-sortable flex')

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

        # Remove None values to use SortableJS defaults
        self._props['options'] = {k: v for k, v in sortable_options.items() if v is not None}


        # When the order of objects have changed, synchronize
        self.on('order_updated', self._synchronize_order)

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


    def _synchronize_order(self, e):
        """Synchronize the Python-side order with the JavaScript DOM order."""
        try:
            if not self.default_slot:
                return

            # If no items or no order data, exit early
            if not self.default_slot.children or 'childrenData' not in e.args:
                return

            if e.args.get('childrenData') is None:
                return

            ordered_items: list[Element] = []

            # First, create a map of ID to item
            # Add "c" in front of ID to match DOMs ID
            id_to_item = {f"c{item.id}": item for item in self.default_slot.children}

            # Then construct the new order based on the DOM order
            for item in e.args.get('childrenData'):
                if item['id'] in id_to_item:
                    ordered_items.append(id_to_item[item['id']])

            # Add any remaining items that might not be in the currentOrder
            for item in self.default_slot.children:
                if str(item.id) not in e.args.get('childrenData') and item not in ordered_items:
                    ordered_items.append(item)

            # Replace the children with the ordered list
            self.default_slot.children = ordered_items
        except Exception as ex:
            print(f"Error synchronizing order: {ex}")

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
        self.run_method('sort', [f"c{item.id}" for item in order], use_animation)

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
