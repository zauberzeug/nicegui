from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

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
        *,
        group: Optional[Union[str, Dict]] = None,
        sort: bool = True,
        delay: int = 0,
        disabled: bool = False,
        animation: int = 150,
        handle: Optional[str] = None,
        filter: Optional[str] = None,
        draggable: str = '>*',  # By default, make all direct children draggable
        ghost_class: Optional[str] = 'sortable-ghost',
        chosen_class: Optional[str] = 'sortable-chosen',
        drag_class: Optional[str] = 'sortable-drag',
        data_id_attr: str = 'id',
        swap_threshold: float = 1,
        fallback_on_body: bool = False,
        # Plugin-specific options
        # MultiDrag plugin
        multi_drag: bool = False,
        multi_drag_key: Optional[str] = None,
        selected_class: str = 'sortable-selected',
        # Swap plugin
        swap: bool = False,
        swap_class: str = 'sortable-swap-highlight',
        # AutoScroll plugin
        auto_scroll: bool = True,
        scroll_sensitivity: int = 30,
        scroll_speed: int = 10,
        # OnSpill plugin options
        remove_on_spill: bool = False,
        revert_on_spill: bool = False,
        # Event callbacks
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
            group: Group name or group options for dragging between lists
            sort: Enable sorting within list
            delay: Time in milliseconds to define when sorting should start
            disabled: Disables the sortable if set to true
            animation: Animation speed in ms, 0 for no animation
            handle: Drag handle selector within list items
            filter: Selectors that do not lead to dragging
            draggable: Specifies which items inside the element should be draggable
            ghost_class: Class name for the drop placeholder
            chosen_class: Class name for the chosen item
            drag_class: Class name for the dragging item
            data_id_attr: HTML attribute that is used by the toArray() method
            swap_threshold: Threshold of the swap zone
            fallback_on_body: Appends the cloned DOM Element into the Document's Body

            # Plugin options
            multi_drag: Enable the MultiDrag plugin for selecting multiple items
            multi_drag_key: Key to hold to select multiple items (e.g., 'ctrl')
            selected_class: Class applied to selected items when using MultiDrag
            swap: Enable the Swap plugin to swap items instead of sorting
            swap_class: Class applied to the swappable item
            auto_scroll: Enable the AutoScroll plugin (enabled by default)
            scroll_sensitivity: Distance in pixels from the edge to start scrolling
            scroll_speed: Scroll speed in pixels per frame
            remove_on_spill: When enabled, spilling items outside the list removes them
            revert_on_spill: When enabled, spilling items outside reverts their position

            # Event callbacks
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

        self.classes('nicegui-sortable')
        plugins = {}

        # MultiDrag plugin
        if multi_drag:
            plugins['multiDrag'] = {
                'multiDragKey': multi_drag_key,
                'selectedClass': selected_class,
            }

        # Swap plugin
        if swap:
            plugins['swap'] = {
                'swapClass': swap_class
            }

        # AutoScroll plugin
        plugins['autoScroll'] = {
            'enabled': auto_scroll,
            'sensitivity': scroll_sensitivity,
            'speed': scroll_speed
        }

        # OnSpill plugin options
        if remove_on_spill:
            plugins['removeOnSpill'] = True

        if revert_on_spill:
            plugins['revertOnSpill'] = True

        # Build options object for SortableJS
        options = {
            'group': group,
            'sort': sort,
            'delay': delay,
            'disabled': disabled,
            'animation': animation,
            'handle': handle,
            'filter': filter,
            'draggable': draggable,
            'ghostClass': ghost_class,
            'chosenClass': chosen_class,
            'dragClass': drag_class,
            'dataIdAttr': data_id_attr,
            'swapThreshold': swap_threshold,
            'fallbackOnBody': fallback_on_body,
            'plugins': plugins
        }

        # Remove None values to use SortableJS defaults
        options = {k: v for k, v in options.items() if v is not None}

        self._props['options'] = options

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
        self.run_method('enable')

    def disable(self) -> None:
        """Disable the sortable instance."""
        self.run_method('disable')

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
