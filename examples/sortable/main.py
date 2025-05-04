from random import randint

from nicegui import ui


def on_end(e):
    ui.notify(f'Item moved from {e.args["oldIndex"]} to {e.args["newIndex"]}')


def on_add(e):
    ui.notify('Item added from another list')


def on_sort(e):
    ui.notify('List order changed')


def on_move(e):
    ui.notify('Item being moved')


def on_clone_add(e):
    ui.notify(f'Cloned item added to the target list at index {e.args["newIndex"]}')


def on_filter(e):
    ui.notify(f'Filtered item was clicked: {e.args["item"]}')


def on_select(e):
    ui.notify(f'Item selected: {e.args["item"]}')


def on_deselect(e):
    ui.notify(f'Item deselected: {e.args["item"]}')


def on_spill(e):
    ui.notify(f'Item spilled: {e.args["item"]}')


# Example 1: Simple List
ui.label("")
with ui.card():
    ui.label('Example 1: Simple List').classes('text-h5')
    ui.label('Basic sortable list with animation')

    with ui.sortable(on_end=on_end, animation=150, ghost_class='nicegui-sortable-ghost') as simple_sortable:
        for i in range(1, 7):
            with ui.card().classes('p-4 mb-2'):
                ui.label(f'Item {i}')

# Control Panel
    ui.label('Control Panel').classes('text-h5')

    with ui.row():
        ui.button('Enable Simple List', on_click=lambda: simple_sortable.enable())
        ui.button('Disable Simple List', on_click=lambda: simple_sortable.disable())
        ui.button('Reverse Order', on_click=lambda: simple_sortable.sort(
            list(reversed(simple_sortable.default_slot.children)), True))


# Example 2: Shared Lists
with ui.card():
    ui.label('Example 2: Shared Lists').classes('text-h5')
    ui.label('You can drag between these two lists:')

    with ui.row():
        with ui.card().classes('w-64'):
            ui.label('List 1').classes('text-h6')
            with ui.sortable(group='shared', animation=150, on_add=on_add, on_sort=on_sort) as list1:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1'):
                        ui.label(f'Item {i}')

        with ui.card().classes('w-64 ml-4'):
            ui.label('List 2').classes('text-h6')
            with ui.sortable(group='shared', animation=150, on_add=on_add, on_sort=on_sort) as list2:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1 bg-yellow-100'):
                        ui.label(f'Item {i}')

# Example 3a: Cloning
with ui.card():
    ui.label('Example 3a: Cloning').classes('text-h5')
    ui.label('Try dragging from one list to another. The item you drag will be cloned and the clone will stay in the original list.')
    ui.label('NOTE! The python object gets moved to the cloned object in the DOM. The original object loses its python object reference.')
    ui.label('Both DOM objects will have the same ID. For true cloning, please look at example 3b')

    with ui.row():
        with ui.card().classes('w-64'):
            ui.label('List 1 (Clone Source)').classes('text-h6')
            with ui.sortable(group={'name': 'clone-example', 'pull': 'clone'},
                             animation=150) as clone_list1:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1'):
                        ui.label(f'Item {i}')

        with ui.card().classes('w-64 ml-4'):
            ui.label('List 2 (Clone Source)').classes('text-h6')
            with ui.sortable(group={'name': 'clone-example', 'pull': 'clone'},
                             animation=150) as clone_list2:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1 bg-yellow-100'):
                        ui.label(f'Item {i}')

# Example 3b: Real Cloning


class ClonableCard(ui.card):
    def __init__(
        self,
        label="Slider",
        bg="",
    ):
        super().__init__()
        self.label = label
        self.bg = bg

        # Create a new card with the same content but possibly different styling
        with self.classes(f'p-2 mb-1 {self.bg}'):
            ui.label(self.label)

    def clone(self):
        return ClonableCard(
            label=f"Clone of {self.label}",
            bg=self.bg,
        )


def on_add_create_clone(e):
    # Get info about the added item
    item_id = e.args.get("item")
    new_index = e.args.get("newIndex")

    # Find the original item in the source list
    # This is where we need to know which list the item came from
    if e.sender is true_clone_list2:
        source_items = true_clone_list1.default_slot.children
    else:
        source_items = true_clone_list2.default_slot.children

    # Find the original item based on DOM ID (removing the "c" prefix)
    original_item = None
    for item in source_items:
        if f"c{item.id}" == item_id:
            original_item = item
            break

    if original_item:
        with e.sender:
            # Get the class of the original item
            item_class = type(original_item)
            if hasattr(original_item, "clone"):
                new_item = original_item.clone()  # type: ignore
            else:
                new_item = item_class()  # fallback
            # Optionally, copy properties from original_item to new_item if needed
            new_item.move(target_index=new_index)


with ui.card():
    ui.label('Example 3b: True Cloning').classes('text-h5')
    ui.label('This is the same example as 3a but instead of making a clone only in the DOM, the clone will get removed and a new python object will be created in its place.')

    with ui.row():
        with ui.card().classes('w-64'):
            ui.label('List 1 (Clone Source)').classes('text-h6')
            with ui.sortable(group={'name': 'true-clone-example', 'pull': 'clone'},
                             animation=150, remove_on_add=True, on_add=on_add_create_clone) as true_clone_list1:
                for i in range(1, 7):
                    ClonableCard(f'Item {i}')

        with ui.card().classes('w-64 ml-4'):
            ui.label('List 2 (Clone Source)').classes('text-h6')
            with ui.sortable(group={'name': 'true-clone-example', 'pull': 'clone'},
                             animation=150, remove_on_add=True, on_add=on_add_create_clone) as true_clone_list2:
                for i in range(1, 7):
                    ClonableCard(f'Item {i}', "bg-yellow-100")

# Example 4: Disabling Sorting
with ui.card():
    ui.label('Example 4: Disabling Sorting').classes('text-h5')
    ui.label('Try sorting the list on the left. It is not possible because it has its "sort" option set to false. However, you can still drag from the list on the left to the list on the right.')

    with ui.row():
        with ui.card().classes('w-64'):
            ui.label('Non-Sortable List (Pull Only)').classes('text-h6')
            with ui.sortable(group={'name': 'shared-disabled', 'pull': 'clone', 'put': False},
                             animation=150, sort=False) as disabled_sort_list1:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1'):
                        ui.label(f'Item {i}')

        with ui.card().classes('w-64 ml-4'):
            ui.label('Sortable List').classes('text-h6')
            with ui.sortable(group='shared-disabled', animation=150) as disabled_sort_list2:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1 bg-yellow-100'):
                        ui.label(f'Item {i}')

# Example 5: Handle Example
with ui.card():
    ui.label('Example 5: Handle').classes('text-h5')
    ui.label('Dragging is only possible using the handle')

    with ui.sortable(handle='.nicegui-sortable-handle', animation=150, on_move=on_move) as handle_sortable:
        for i in range(1, 7):
            with ui.card().classes('p-2 mb-1'):
                with ui.row().classes('items-center w-full'):
                    ui.icon('drag_handle').classes("nicegui-sortable-handle")
                    ui.label(f'Item {i}')

# Example 6: Filter Example
with ui.card():
    ui.label('Example 6: Filter').classes('text-h5')
    ui.label('Try dragging the item with a red background. It cannot be done, because that item is filtered out using the "filter" option.')

    with ui.sortable(filter='.nicegui-sortable-filtered', animation=150, on_filter=on_filter) as filter_sortable:
        for i in range(1, 7):
            if i == 4:
                with ui.card().classes('p-2 mb-1 nicegui-sortable-filtered bg-red-200'):
                    ui.label('Filtered').classes('text-red-800')
            else:
                with ui.card().classes('p-2 mb-1'):
                    ui.label(f'Item {i}')

# Example 7: Thresholds
with ui.card():
    ui.label('Example 7: Thresholds').classes('text-h5')
    ui.label('This example demonstrates how swap thresholds affect drag and drop behavior.')

    with ui.row():
        ui.label('Swap Threshold')
        swap_threshold = ui.slider(min=0, max=1, value=0.5, step=0.01).props('label-always')
        invert_swap = ui.checkbox('Invert Swap')

    # First add tabbed navigation for vertical vs horizontal examples
    with ui.tabs().classes('w-full') as tabs:
        vertical_tab = ui.tab('Vertical List')
        horizontal_tab = ui.tab('Horizontal List')

    with ui.tab_panels(tabs, value=vertical_tab).classes('w-full'):
        # Vertical list panel
        with ui.tab_panel(vertical_tab):
            # Create a container for visual indicators
            vertical_cards = []

            with ui.element('div').classes('square-section'):
                with ui.sortable(
                    animation=150,
                    swap_threshold=0.5,  # Initial value
                    inverted_swap_threshold=0.5  # Add this initial value
                ) as vertical_sortable:
                    for i in range(1, 5):
                        with ui.card().classes('p-4 m-2 bg-blue-100 threshold-card') as card:
                            north_indicator = ui.element('div').classes('swap-zone-indicator north').style(
                                'position: absolute; background-color: rgba(255,0,0,0.2); ' +
                                'width: 100%; left: 0; transition: all 0.3s ease;'
                            )
                            south_indicator = ui.element('div').classes('swap-zone-indicator south').style(
                                'position: absolute; background-color: rgba(255,0,0,0.2); ' +
                                'width: 100%; left: 0; transition: all 0.3s ease;'
                            )

                            vertical_cards.append((north_indicator, south_indicator))
                            ui.label(f'Drag me {i}').classes('text-center')

        # Horizontal list panel
        with ui.tab_panel(horizontal_tab):
            # Create a container for horizontal visual indicators
            horizontal_cards = []

            with ui.element('div').classes('square-section flex justify-center'):
                with ui.sortable(
                    animation=150,
                    direction='horizontal',  # Set direction to horizontal
                    swap_threshold=0.5,
                    inverted_swap_threshold=0.5
                ).classes('flex flex-row') as horizontal_sortable:
                    for i in range(1, 5):
                        with ui.card().classes('p-4 m-2 bg-green-100 horizontal-threshold-card') as card:
                            west_indicator = ui.element('div').classes('swap-zone-indicator west').style(
                                'position: absolute; background-color: rgba(255,0,0,0.2); ' +
                                'height: 100%; top: 0; transition: all 0.3s ease;'
                            )
                            east_indicator = ui.element('div').classes('swap-zone-indicator east').style(
                                'position: absolute; background-color: rgba(255,0,0,0.2); ' +
                                'height: 100%; top: 0; transition: all 0.3s ease;'
                            )

                            horizontal_cards.append((west_indicator, east_indicator))
                            ui.label(f'Drag {i}').classes('text-center')

    # Update both vertical and horizontal thresholds when the slider changes
    def update_threshold_ui(e=None):
        threshold_value = swap_threshold.value
        invert_value = invert_swap.value

        # Update vertical sortable
        vertical_sortable.swap_threshold = threshold_value
        vertical_sortable.inverted_swap_threshold = threshold_value
        vertical_sortable.invert_swap = invert_value

        # Update horizontal sortable
        horizontal_sortable.swap_threshold = threshold_value
        horizontal_sortable.inverted_swap_threshold = threshold_value
        horizontal_sortable.invert_swap = invert_value

        # Update vertical indicators
        for north, south in vertical_cards:
            indicator_height = threshold_value * 100

            if invert_value:
                # In inverted mode, indicators move to edges
                north.style(
                    f'height: {indicator_height/2}%; top: auto; ' +
                    'bottom: 0; transform: none;'
                )
                south.style(
                    f'height: {indicator_height/2}%; bottom: auto; ' +
                    'top: 0; transform: none;'
                )
            else:
                # In normal mode, both indicators stack in the center
                north.style(
                    f'height: {indicator_height}%; top: 50%; transform: translateY(-50%);'
                )
                south.style(
                    f'height: {indicator_height}%; top: 50%; transform: translateY(-50%);'
                )

        # Update horizontal indicators
        for west, east in horizontal_cards:
            indicator_width = threshold_value * 100

            if invert_value:
                # In inverted mode, indicators move to edges
                west.style(
                    f'width: {indicator_width/2}%; left: auto; ' +
                    'right: 0; transform: none;'
                )
                east.style(
                    f'width: {indicator_width/2}%; right: auto; ' +
                    'left: 0; transform: none;'
                )
            else:
                # In normal mode, both indicators stack in the center
                west.style(
                    f'width: {indicator_width}%; left: 50%; transform: translateX(-50%);'
                )
                east.style(
                    f'width: {indicator_width}%; left: 50%; transform: translateX(-50%);'
                )

        ui.notify(f'Updated threshold to {threshold_value}, invert: {invert_value}')

    # Initialize the display
    update_threshold_ui()

    # Add event handlers for UI controls
    swap_threshold.on('update:model-value', update_threshold_ui)
    invert_swap.on('update:model-value', update_threshold_ui)

    # Add supporting CSS
    ui.add_css("""
    .threshold-card {
        position: relative;
        min-height: 80px;
        width: 100%;
    }
    .horizontal-threshold-card {
        position: relative;
        height: 80px;
        width: 120px;
    }
    .swap-zone-indicator {
        pointer-events: none;
        z-index: 10;
    }
    .swap-zone-indicator.north {
        border-top: 2px dashed rgba(255,0,0,0.5);
    }
    .swap-zone-indicator.south {
        border-bottom: 2px dashed rgba(255,0,0,0.5);
    }
    .swap-zone-indicator.west {
        border-left: 2px dashed rgba(255,0,0,0.5);
    }
    .swap-zone-indicator.east {
        border-right: 2px dashed rgba(255,0,0,0.5);
    }
    """)

# Example 8: Grid
with ui.card():
    ui.label('Example 8: Grid').classes('text-h5')
    ui.label('This example shows how to create a sortable grid layout.')

    with ui.element('div').classes("w-96"):
        with ui.sortable(
            animation=150,
            delay=150,  # Adding a small delay helps with touch devices
        ).classes('flex flex-wrap') as grid_sortable:
            for i in range(1, 21):
                with ui.card().classes('grid-square w-20 m-1 p-2 items-center justify-center'):
                    ui.label(f'Item {i}')


# Example 9: Nested Sortables
with ui.card():
    ui.label('Example 9: Nested Sortables').classes('text-h5')
    ui.label('This example demonstrates nested sortable lists where items can be dragged between different levels.')
    ui.label('Note: When using nested Sortables with animation, it is recommended to set fallbackOnBody to true and to either set invertSwap to true or use a lower swapThreshold value.')

    # Create a helper function to recursively initialize nested sortables
    def create_nested_list(items, level=1):
        with ui.sortable(
            group='nested',
            animation=150,
            fallback_on_body=True,
            swap_threshold=0.4,
            invert_swap=True,
            empty_insert_threshold=10,
            delay=150,
        ).classes(f'nicegui-sortable-nested level-{level}'):
            for item in items:
                with ui.card().classes(f'p-3 mb-2 nested-item level-{level}'):
                    ui.label(item['text']).classes('font-bold')
                    # Create a container for children regardless of whether they exist
                    with ui.element('div').classes('pl-4 border-l-2 border-gray-300 nested-children'):
                        children = item.get('children', [])
                        create_nested_list(children, level + 1)

    # Define the nested structure
    nested_data = [
        {
            'text': 'Item 1.1',
            'children': [
                {'text': 'Item 2.1'},
                {
                    'text': 'Item 2.2',
                    'children': [
                        {'text': 'Item 3.1'},
                        {'text': 'Item 3.2'},
                        {'text': 'Item 3.3'},
                        {'text': 'Item 3.4'}
                    ]
                },
                {'text': 'Item 2.3'},
                {'text': 'Item 2.4'}
            ]
        },
        {'text': 'Item 1.2'},
        {'text': 'Item 1.3'},
        {
            'text': 'Item 1.4',
            'children': [
                {'text': 'Item 2.5'},
                {'text': 'Item 2.6'},
                {'text': 'Item 2.7'},
                {'text': 'Item 2.8'}
            ]
        },
        {'text': 'Item 1.5'}
    ]

    with ui.element('div').classes('nested-container'):
        create_nested_list(nested_data)

    # Add improved supporting styles for the nested sortables
    ui.add_css("""
    /* Basic styling for nested items */
    .nested-item {
        background-color: #f8f9fa;
        transition: background-color 0.2s;
    }

    /* Color differentiation by nesting level */
    .level-1 {
        background-color: #f8f9fa;
    }

    .level-2 {
        background-color: #e9ecef;
    }

    .level-3 {
        background-color: #dee2e6;
    }

    /* Hover effect */
    .nested-item:hover {
        background-color: #e2e8f0;
    }

    /* Empty sortable containers styling */
    .nicegui-sortable-nested:empty {
        background-color: rgba(0,0,255,0.05);
    }

    /* Highlight empty containers on hover for better UX */
    .nested-children:hover .nicegui-sortable-nested:empty {
        background-color: rgba(0,0,255,0.1);
        border-color: #aaa;
    }
    """)

# Example 10: MultiDrag Plugin
with ui.card():
    ui.label('Example 10: MultiDrag Plugin').classes('text-h5')
    ui.label('Hold down Ctrl/Cmd key while selecting items to select multiple. Then drag them as a group.')

    with ui.sortable(
        animation=150,
        multi_drag=True,
        multi_drag_key='ctrl',
        multi_drag_class='nicegui-sortable-multi-selected',
        on_select=on_select,
        on_deselect=on_deselect
    ) as multi_drag_sortable:
        for i in range(1, 7):
            with ui.card().classes('p-2 mb-1'):
                ui.label(f'Item {i} (hold Ctrl/Cmd to select multiple)')

# Example 11: Swap Plugin
with ui.card():
    ui.label('Example 11: Swap Plugin').classes('text-h5')
    ui.label('Items will swap places instead of sorting when dragged over each other.')

    with ui.sortable(
        animation=150,
        swap=True,
        swap_class='nicegui-sortable-swap-highlight'
    ) as swap_sortable:
        for i in range(1, 7):
            with ui.card().classes('p-2 mb-1'):
                ui.label(f'Item {i} (will swap instead of sort)')

# Example 12: OnSpill Plugins - Remove and Revert
with ui.card():
    ui.label('Example 12: OnSpill Plugins').classes('text-h5')
    with ui.row():
        with ui.card().classes('w-64 mr-4'):
            ui.label('RemoveOnSpill Plugin').classes('text-h5')
            ui.label('Drag an item outside the list to remove it.')

            with ui.sortable(
                animation=150,
                remove_on_spill=True,
                on_spill=on_spill
            ) as remove_spill_sortable:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1 bg-red-100'):
                        ui.label(f'Drag outside to remove {i}')

        with ui.card().classes('w-64'):
            ui.label('RevertOnSpill Plugin').classes('text-h5')
            ui.label('Drag an item outside the list and it will revert to original position.')

            with ui.sortable(
                animation=150,
                revert_on_spill=True,
                on_spill=on_spill
            ) as revert_spill_sortable:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1 bg-green-100'):
                        ui.label(f'Drag outside to revert {i}')

# Example 13: AutoScroll Plugin
with ui.card():
    ui.label('Example 13: AutoScroll Plugin').classes('text-h5')
    ui.label('This example demonstrates auto-scrolling when dragging near the edges of the container.')

    with ui.element('div').style('max-height: 300px; overflow-y: auto; padding: 10px;'):
        with ui.sortable(
            animation=150,
            auto_scroll=True,
            scroll_sensitivity=20,
            scroll_speed=15
        ) as auto_scroll_sortable:
            for i in range(1, 15):
                with ui.card().classes('p-2 mb-1'):
                    ui.label(f'Item {i} (drag up/down to auto-scroll)')


# Example 14: Add/Remove Items in Sortable List
def add_deletable_object(label: str):
    with ui.card().classes('p-2 mb-1'):
        with ui.row().classes('items-center w-full'):
            ui.label(label).classes('flex-grow')
            ui.button(icon='delete', color='red',
                      on_click=lambda e: e.sender.parent_slot.parent.parent_slot.parent.delete()).classes('min-w-0 w-8 h-8')


def add_new_item(string: str):
    with dynamic_sortable:
        add_deletable_object(string)
    ui.notify('Item added to the list')


with ui.card():
    ui.label('Example 14: Add/Remove Items').classes('text-h5')
    ui.label('This example shows how to dynamically add and remove items from a sortable list.')

    # Form for adding new items
    with ui.row().classes('w-full items-center mb-4'):
        new_item_input = ui.input('Enter new item text').classes('flex-grow mr-2')
        ui.button('Add Item', on_click=lambda: add_new_item(new_item_input.value)).classes('bg-green-500')
        new_item_input.value = ''  # Clear the input

    with ui.sortable(
        animation=150,
        on_end=on_end,
        fallback_on_body=True,
    ) as dynamic_sortable:
        # Pre-populate with some items
        for i in range(1, 5):
            add_deletable_object(f'Sortable Item {i} - Drag to reorder')

    # Action buttons
    with ui.row().classes('mt-4'):
        ui.button('Delete All', color='red', on_click=lambda: dynamic_sortable.clear()).classes('mr-2')
        ui.button('Add 3 Items', color='green', on_click=lambda: [
                  add_new_item(str(randint(1, 100))) for _ in range(3)]).classes('mr-2')

        async def show_current_order():
            items_text = [item.default_slot.children[0].default_slot.children[0].text
                          for item in dynamic_sortable.default_slot.children]
            ui.notify(f'Current order: {items_text}')

        ui.button('Show Current Order', on_click=show_current_order)

ui.run(
    title="SortableJS Complete Plugin Examples",
    native=True,
    reload=True
)
