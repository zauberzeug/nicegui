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
        *,
        group: Optional[Union[str, Dict]] = None,
        sort: bool = True,
        delay: int = 0,
        delay_on_touch_only: bool = False,
        touch_start_threshold: int = 0,
        disabled: bool = False,
        store: Optional[Dict] = None,
        animation: int = 150,
        easing: Optional[str] = "cubic-bezier(1, 0, 0, 1)",
        handle: Optional[str] = None,
        filter: Optional[str] = None,
        prevent_on_filter: bool = True,
        draggable: str = '>*',  # By default, make all direct children draggable
        ghost_class: Optional[str] = None,
        chosen_class: Optional[str] = None,
        drag_class: Optional[str] = None,
        data_id_attr: str = 'id',
        swap_threshold: float = 1,
        invert_swap: bool = False,
        inverted_swap_threshold: Optional[float] = 1,
        direction: Optional[str] = None,
        force_fallback: bool = False,
        fallback_class: Optional[str] = "nicegui-sortable-fallback",
        fallback_on_body: bool = False,
        fallback_tolerance: int = 0,
        dragover_bubble: bool = False,
        remove_clone_on_hide: bool = True,
        empty_insert_threshold: int = 5,
        # Plugin-specific options
        # MultiDrag plugin
        multi_drag: bool = False,
        multi_drag_key: Optional[str] = None,
        multi_drag_class: str = 'nicegui-sortable-multi-selected',
        multi_drag_avoid_implicit_deselect: bool = False,
        # Swap plugin
        swap: bool = False,
        swap_class: str = 'nicegui-sortable-swap-highlight',
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
            group: Group name or group options for dragging between lists. Can be a string or a dict like 
                   {'name': '...', 'pull': [True, False, 'clone', array], 'put': [True, False, array]}
            sort: Enable sorting within list
            delay: Time in milliseconds to define when sorting should start
            delay_on_touch_only: Only delay if user is using touch
            touch_start_threshold: Px, how many pixels the point should move before cancelling a delayed drag event
            disabled: Disables the sortable if set to true
            store: Object with save/get methods to save/restore list state
            animation: Animation speed in ms, 0 for no animation
            easing: Easing for animation. Example: "cubic-bezier(1, 0, 0, 1)". See https://easings.net/ for examples
            handle: Drag handle selector within list items (e.g., ".my-handle")
            filter: Selectors that do not lead to dragging (e.g., ".ignore-elements")
            prevent_on_filter: Call event.preventDefault() when triggered filter
            draggable: Specifies which items inside the element should be draggable (e.g., ".item")
            ghost_class: Class name for the drop placeholder
            chosen_class: Class name for the chosen item
            drag_class: Class name for the dragging item
            data_id_attr: HTML attribute that is used by the toArray() method
            swap_threshold: Threshold of the swap zone
            invert_swap: Will always use inverted swap zone if set to true
            inverted_swap_threshold: Threshold of the inverted swap zone
            direction: Direction of Sortable (horizontal/vertical, auto-detected if not given)
            force_fallback: Ignore the HTML5 DnD behavior and force the fallback to kick in
            fallback_class: Class name for the cloned DOM Element when using forceFallback
            fallback_on_body: Appends the cloned DOM Element into the Document's Body
            fallback_tolerance: Specify in pixels how far the mouse should move before it's considered a drag
            dragover_bubble: Whether to allow event bubbling for dragover events
            remove_clone_on_hide: Remove the clone element when it is not showing, rather than just hiding it
            empty_insert_threshold: Distance mouse must be from empty sortable to insert drag element

            # Plugin options
            multi_drag: Enable the MultiDrag plugin for selecting multiple items
            multi_drag_key: Key to hold to select multiple items (e.g., 'ctrl')
            multi_drag_class: Class applied to selected items when using MultiDrag
            multi_drag_avoid_implicit_deselect: Avoid deselecting items when clicking outside the list
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
        sortable_options = {}

        # MultiDrag plugin
        sortable_options.update({
            'multiDrag': multi_drag,
            'multiDragKey': multi_drag_key,
            'selectedClass': multi_drag_class,
            'avoidImplicitDeselect': multi_drag_avoid_implicit_deselect
        })

        # Swap plugin
        sortable_options.update({
            'swap': swap,
            'swapClass': swap_class
        })

        # AutoScroll plugin
        sortable_options.update({
            'scroll': auto_scroll,
            'scrollSensitivity': scroll_sensitivity,
            'scrollSpeed': scroll_speed
        })

        # OnSpill plugin options
        if remove_on_spill:
            plugins['removeOnSpill'] = True

        if revert_on_spill:
            plugins['revertOnSpill'] = True

        # Build options object for SortableJS
        sortable_options.update({
            'group': group,
            'sort': sort,
            'delay': delay,
            'delayOnTouchOnly': delay_on_touch_only,
            'touchStartThreshold': touch_start_threshold,
            'disabled': disabled,
            'store': store,
            'animation': animation,
            'easing': easing,
            'handle': handle,
            'filter': filter,
            'preventOnFilter': prevent_on_filter,
            'draggable': draggable,
            'ghostClass': ghost_class,
            'chosenClass': chosen_class,
            'dragClass': drag_class,
            'dataIdAttr': data_id_attr,
            'swapThreshold': swap_threshold,
            'invertSwap': invert_swap,
            'invertedSwapThreshold': inverted_swap_threshold,
            'direction': direction,
            'forceFallback': force_fallback,
            'fallbackClass': fallback_class,
            'fallbackOnBody': fallback_on_body,
            'fallbackTolerance': fallback_tolerance,
            'dragoverBubble': dragover_bubble,
            'removeCloneOnHide': remove_clone_on_hide,
            'emptyInsertThreshold': empty_insert_threshold,
            'plugins': plugins
        })

        # Remove None values to use SortableJS defaults
        sortable_options = {k: v for k, v in sortable_options.items() if v is not None}

        self._props['options'] = sortable_options

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

    @property
    def group(self) -> str | None:
        return self._props['options']['group']

    @group.setter
    def group(self, value: str | None):
        self._props['options']['group'] = value
        self.run_method('setOption', 'group', value)

    @property
    def sort(self) -> bool | None:
        return self._props['options']['sort']

    @sort.setter
    def sort(self, value: bool | None):
        self._props['options']['sort'] = value
        self.run_method('setOption', 'sort', value)

    @property
    def delay(self) -> int | None:
        return self._props['options']['delay']

    @delay.setter
    def delay(self, value: int | None):
        self._props['options']['delay'] = value
        self.run_method('setOption', 'delay', value)

    @property
    def delay_on_touch_only(self) -> bool | None:
        return self._props['options']['delayOnTouchOnly']

    @delay_on_touch_only.setter
    def delay_on_touch_only(self, value: bool | None):
        self._props['options']['delayOnTouchOnly'] = value
        self.run_method('setOption', 'delayOnTouchOnly', value)

    @property
    def touch_start_threshold(self) -> int | None:
        return self._props['options']['touchStartThreshold']

    @touch_start_threshold.setter
    def touch_start_threshold(self, value: int | None):
        self._props['options']['touchStartThreshold'] = value
        self.run_method('setOption', 'touchStartThreshold', value)

    @property
    def disabled(self) -> bool | None:
        return self._props['options']['disabled']

    @disabled.setter
    def disabled(self, value: bool | None):
        self._props['options']['disabled'] = value
        self.run_method('setOption', 'disabled', value)

    @property
    def store(self) -> dict | None:
        return self._props['options']['store']

    @store.setter
    def store(self, value: dict | None):
        self._props['options']['store'] = value
        self.run_method('setOption', 'store', value)

    @property
    def animation(self) -> int | None:
        return self._props['options']['animation']

    @animation.setter
    def animation(self, value: int | None):
        self._props['options']['animation'] = value
        self.run_method('setOption', 'animation', value)

    @property
    def easing(self) -> str | None:
        return self._props['options']['easing']

    @easing.setter
    def easing(self, value: str | None):
        self._props['options']['easing'] = value
        self.run_method('setOption', 'easing', value)

    @property
    def handle(self) -> str | None:
        return self._props['options']['handle']

    @handle.setter
    def handle(self, value: str | None):
        self._props['options']['handle'] = value
        self.run_method('setOption', 'handle', value)

    @property
    def filter(self) -> str | None:
        return self._props['options']['filter']

    @filter.setter
    def filter(self, value: str | None):
        self._props['options']['filter'] = value
        self.run_method('setOption', 'filter', value)

    @property
    def prevent_on_filter(self) -> bool | None:
        return self._props['options']['preventOnFilter']

    @prevent_on_filter.setter
    def prevent_on_filter(self, value: bool | None):
        self._props['options']['preventOnFilter'] = value
        self.run_method('setOption', 'preventOnFilter', value)

    @property
    def draggable(self) -> bool | None:
        return self._props['options']['draggable']

    @draggable.setter
    def draggable(self, value: bool | None):
        self._props['options']['draggable'] = value
        self.run_method('setOption', 'draggable', value)

    @property
    def ghost_class(self) -> str | None:
        return self._props['options']['ghostClass']

    @ghost_class.setter
    def ghost_class(self, value: str | None):
        self._props['options']['ghostClass'] = value
        self.run_method('setOption', 'ghostClass', value)

    @property
    def chosen_class(self) -> str | None:
        return self._props['options']['chosenClass']

    @chosen_class.setter
    def chosen_class(self, value: str | None):
        self._props['options']['chosenClass'] = value
        self.run_method('setOption', 'chosenClass', value)

    @property
    def drag_class(self) -> str | None:
        return self._props['options']['dragClass']

    @drag_class.setter
    def drag_class(self, value: str | None):
        self._props['options']['dragClass'] = value
        self.run_method('setOption', 'dragClass', value)

    @property
    def data_id_attr(self) -> str | None:
        return self._props['options']['dataIdAttr']

    @data_id_attr.setter
    def data_id_attr(self, value: str | None):
        self._props['options']['dataIdAttr'] = value
        self.run_method('setOption', 'dataIdAttr', value)

    @property
    def swap_threshold(self) -> str | None:
        return self._props['options']['swapThreshold']

    @swap_threshold.setter
    def swap_threshold(self, value: str | None):
        self._props['options']['swapThreshold'] = value
        self.run_method('setOption', 'swapThreshold', value)

    @property
    def invert_swap(self) -> bool | None:
        return self._props['options']['invertSwap']

    @invert_swap.setter
    def invert_swap(self, value: bool | None):
        self._props['options']['invertSwap'] = value
        self.run_method('setOption', 'invertSwap', value)

    @property
    def inverted_swap_threshold(self) -> float | None:
        return self._props['options']['invertedSwapThreshold']

    @inverted_swap_threshold.setter
    def inverted_swap_threshold(self, value: float | None):
        self._props['options']['invertedSwapThreshold'] = value
        self.run_method('setOption', 'invertedSwapThreshold', value)

    @property
    def direction(self) -> str | None:
        return self._props['options']['direction']

    @direction.setter
    def direction(self, value: str | None):
        self._props['options']['direction'] = value
        self.run_method('setOption', 'direction', value)

    @property
    def force_fallback(self) -> bool | None:
        return self._props['options']['forceFallback']

    @force_fallback.setter
    def force_fallback(self, value: bool | None):
        self._props['options']['forceFallback'] = value
        self.run_method('setOption', 'forceFallback', value)

    @property
    def fallback_class(self) -> str | None:
        return self._props['options']['fallbackClass']

    @fallback_class.setter
    def fallback_class(self, value: str | None):
        self._props['options']['fallbackClass'] = value
        self.run_method('setOption', 'fallbackClass', value)

    @property
    def fallback_on_body(self) -> int | None:
        return self._props['options']['fallbackOnBody']

    @fallback_on_body.setter
    def fallback_on_body(self, value: int | None):
        self._props['options']['fallbackOnBody'] = value
        self.run_method('setOption', 'fallbackOnBody', value)

    @property
    def fallback_tolerance(self) -> int | None:
        return self._props['options']['fallbackTolerance']

    @fallback_tolerance.setter
    def fallback_tolerance(self, value: int | None):
        self._props['options']['fallbackTolerance'] = value
        self.run_method('setOption', 'fallbackTolerance', value)

    @property
    def dragover_bubble(self) -> bool | None:
        return self._props['options']['dragoverBubble']

    @dragover_bubble.setter
    def dragover_bubble(self, value: bool | None):
        self._props['options']['dragoverBubble'] = value
        self.run_method('setOption', 'dragoverBubble', value)

    @property
    def remove_clone_on_hide(self) -> bool | None:
        return self._props['options']['removeCloneOnHide']

    @remove_clone_on_hide.setter
    def remove_clone_on_hide(self, value: bool | None):
        self._props['options']['removeCloneOnHide'] = value
        self.run_method('setOption', 'removeCloneOnHide', value)

    @property
    def empty_insert_threshold(self) -> int | None:
        return self._props['options']['emptyInsertThreshold']

    @empty_insert_threshold.setter
    def empty_insert_threshold(self, value: int | None):
        self._props['options']['emptyInsertThreshold'] = value
        self.run_method('setOption', 'emptyInsertThreshold', value)

    @property
    def multi_drag(self) -> bool | None:
        return self._props['options']['multiDrag']

    @multi_drag.setter
    def multi_drag(self, value: bool | None):
        self._props['options']['multiDrag'] = value
        self.run_method('setOption', 'multiDrag', value)

    @property
    def multi_drag_key(self) -> str | None:
        return self._props['options']['multiDragKey']

    @multi_drag_key.setter
    def multi_drag_key(self, value: str | None):
        self._props['options']['multiDragKey'] = value
        self.run_method('setOption', 'multiDragKey', value)

    @property
    def multi_drag_class(self) -> str | None:
        return self._props['options']['selectedClass']

    @multi_drag_class.setter
    def multi_drag_class(self, value: str | None):
        self._props['options']['selectedClass'] = value
        self.run_method('setOption', 'selectedClass', value)

    @property
    def multi_drag_avoid_implicit_deselect(self) -> bool | None:
        return self._props['options']['avoidImplicitDeselect']

    @multi_drag_avoid_implicit_deselect.setter
    def multi_drag_avoid_implicit_deselect(self, value: bool | None):
        self._props['options']['avoidImplicitDeselect'] = value
        self.run_method('setOption', 'avoidImplicitDeselect', value)

    @property
    def swap(self) -> bool | None:
        return self._props['options']['swap']

    @swap.setter
    def swap(self, value: bool | None):
        self._props['options']['swap'] = value
        self.run_method('setOption', 'swap', value)

    @property
    def swap_class(self) -> str | None:
        return self._props['options']['swapClass']

    @swap_class.setter
    def swap_class(self, value: str | None):
        self._props['options']['swapClass'] = value
        self.run_method('setOption', 'swapClass', value)

    @property
    def auto_scroll(self) -> bool | None:
        return self._props['options']['scroll']

    @auto_scroll.setter
    def auto_scroll(self, value: bool | None):
        self._props['options']['scroll'] = value
        self.run_method('setOption', 'scroll', value)

    @property
    def auto_scroll_sensitivity(self) -> int | None:
        return self._props['options']['scrollSensitivity']

    @auto_scroll_sensitivity.setter
    def auto_scroll_sensitivity(self, value: int | None):
        self._props['options']['scrollSensitivity'] = value
        self.run_method('setOption', 'scrollSensitivity', value)

    @property
    def auto_scroll_speed(self) -> int | None:
        return self._props['options']['scrollSpeed']

    @auto_scroll_speed.setter
    def auto_scroll_speed(self, value: int | None):
        self._props['options']['scrollSpeed'] = value
        self.run_method('setOption', 'scrollSpeed', value)

    @property
    def remove_on_spill(self) -> bool | None:
        return self._props['options']['removeOnSpill']

    @remove_on_spill.setter
    def remove_on_spill(self, value: bool | None):
        self._props['options']['removeOnSpill'] = value
        self.run_method('setOption', 'removeOnSpill', value)

    @property
    def revert_on_spill(self) -> bool | None:
        return self._props['options']['revertOnSpill']

    @revert_on_spill.setter
    def revert_on_spill(self, value: bool | None):
        self._props['options']['revertOnSpill'] = value
        self.run_method('setOption', 'revertOnSpill', value)

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

    def remove_item_by_id(self, item_id: str) -> None:
        """Remove an item from the sortable by its DOM ID.

        This is useful for handling custom drag-and-drop operations where you need
        to remove auto-created clones from the DOM.

        Args:
            item_id: The DOM ID of the element to remove
        """
        self.run_method('removeItemById', item_id)
