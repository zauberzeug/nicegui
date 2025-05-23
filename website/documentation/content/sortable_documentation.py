from nicegui import ui
from nicegui.events import GenericEventArguments

from random import randint

from . import doc


# Event handlers
def on_end(e: GenericEventArguments):
    ui.notify(f'Item moved from {e.args["oldIndex"]} to {e.args["newIndex"]}')


def on_add():
    ui.notify('Item added from another list')


def on_sort():
    ui.notify('List order changed')


def on_move():
    ui.notify('Item being moved')


def on_clone_add(e: GenericEventArguments):
    ui.notify(f'Cloned item added to the target list at index {e.args["newIndex"]}')


def on_filter(e: GenericEventArguments):
    ui.notify(f'Filtered item was clicked: {e.args["item"]}')


def on_select(e: GenericEventArguments):
    ui.notify(f'Item selected: {e.args["item"]}')


def on_deselect(e: GenericEventArguments):
    ui.notify(f'Item deselected: {e.args["item"]}')


def on_spill(e: GenericEventArguments):
    ui.notify(f'Item spilled: {e.args["item"]}')


@doc.demo(ui.sortable)
def main_demo() -> None:
    with ui.sortable(on_end=on_end):
        for i in range(1, 7):
            with ui.card():
                ui.label(f'Item {i}')


@doc.demo('Control Panel', '''
    You can enable, disable, and manipulate the sortable list programmatically.
''')
def control_panel() -> None:
    with ui.sortable(on_end=on_end) as simple_sortable:
        for i in range(1, 7):
            with ui.card():
                ui.label(f'Item {i}')

    with ui.row():
        ui.button('Enable', on_click=simple_sortable.enable)
        ui.button('Disable', on_click=simple_sortable.disable)
        ui.button('Reverse Order', on_click=lambda: simple_sortable.sort(
            list(reversed(simple_sortable.default_slot.children)), True))


@doc.demo('Shared Lists', '''
    You can enable drag and drop between multiple sortable lists by assigning them to the same group.
''')
def shared_lists() -> None:
    with ui.row():
        with ui.card():
            ui.label('List 1').classes('text-h6')
            with ui.sortable({'group': 'shared'}, on_add=on_add, on_sort=on_sort):
                for i in range(1, 7):
                    with ui.card():
                        ui.label(f'Item {i}')

        with ui.card():
            ui.label('List 2').classes('text-h6')
            with ui.sortable({'group': 'shared'}, on_add=on_add, on_sort=on_sort):
                for i in range(1, 7):
                    with ui.card().classes('bg-amber-500'):
                        ui.label(f'Item {i}')


@doc.demo('Cloning', '''
    Items can be cloned when dragging from one list to another, keeping the original item in place.
    NOTE: The python object gets moved to the cloned object in the DOM.
          The original object loses its python object reference.
''')
def cloning() -> None:
    with ui.row():
        with ui.card():
            ui.label('List 1').classes('text-h6')
            with ui.sortable({'group': {'name': 'clone-example', 'pull': 'clone'}}):
                for i in range(1, 7):
                    with ui.card():
                        ui.label(f'Item {i}')

        with ui.card():
            ui.label('List 2').classes('text-h6')
            with ui.sortable({'group': {'name': 'clone-example', 'pull': 'clone'}}):
                for i in range(1, 7):
                    with ui.card().classes('bg-amber-500'):
                        ui.label(f'Item {i}')


@doc.demo('True Cloning', '''
    This is an advanced example that creates true Python object clones when items are dragged between lists.
''')
def true_cloning() -> None:
    class ClonableCard(ui.card):
        def __init__(
            self,
            label='Slider',
            bg='',
        ):
            super().__init__()
            self.label = label
            self.bg = bg

            # Create a new card with the same content but possibly different styling
            with self.classes(f'{self.bg}'):
                ui.label(self.label)

        def clone(self):
            return ClonableCard(
                label=f'Clone of {self.label}',
                bg=self.bg,
            )

    def on_add_create_clone(e):
        # Get info about the added item
        item_id = e.args.get('item')
        new_index = e.args.get('newIndex')

        # Find the original item in the source list
        # This is where we need to know which list the item came from
        if e.sender is true_clone_list2:
            source_items = true_clone_list1.default_slot.children
        else:
            source_items = true_clone_list2.default_slot.children

        # Find the original item based on DOM ID (removing the "c" prefix)
        original_item = None
        for item in source_items:
            if f'c{item.id}' == item_id:
                original_item = item
                break

        if original_item:
            with e.sender:
                # Get the class of the original item
                item_class = type(original_item)
                if hasattr(original_item, 'clone'):
                    new_item = original_item.clone()  # type: ignore
                else:
                    new_item = item_class()  # fallback
                # Optionally, copy properties from original_item to new_item if needed
                new_item.move(target_index=new_index)

    with ui.row():
        with ui.card():
            ui.label('List 1').classes('text-h6')
            with ui.sortable({
                'group': {'name': 'true-clone-example', 'pull': 'clone'},
                'removeOnAdd': True
            }, on_add=on_add_create_clone) as true_clone_list1:
                for i in range(1, 7):
                    ClonableCard(f'Item {i}')

        with ui.card():
            ui.label('List 2').classes('text-h6')
            with ui.sortable({
                'group': {'name': 'true-clone-example', 'pull': 'clone'},
                'removeOnAdd': True
            }, on_add=on_add_create_clone) as true_clone_list2:
                for i in range(1, 7):
                    ClonableCard(f'Item {i}', 'bg-amber-500')


@doc.demo('Disabling Sorting', '''
    You can disable sorting within a list but still allow items to be dragged to other lists.
''')
def disable_sorting() -> None:
    with ui.row():
        with ui.card():
            ui.label('Non-Sortable List (Pull Only)').classes('text-h6')
            with ui.sortable({
                'group': {'name': 'shared-disabled', 'pull': 'clone', 'put': False},
                'sort': False
            }):
                for i in range(1, 7):
                    with ui.card():
                        ui.label(f'Item {i}')

        with ui.card():
            ui.label('Sortable List').classes('text-h6')
            with ui.sortable({'group': 'shared-disabled'}):
                for i in range(1, 7):
                    with ui.card().classes('bg-amber-500'):
                        ui.label(f'Item {i}')


@doc.demo('Handle', '''
    You can restrict dragging to a specific handle element within each item.
''')
def handle_example() -> None:
    with ui.sortable({'handle': '.nicegui-sortable-handle'}, on_move=on_move):
        for i in range(1, 7):
            with ui.card():
                with ui.row().classes('items-center w-full'):
                    ui.icon('drag_handle').classes('nicegui-sortable-handle')
                    ui.label(f'Item {i}')


@doc.demo('Filter', '''
    You can prevent specific items from being draggable by applying a filter.
''')
def filter_example() -> None:
    with ui.sortable({'filter': '.nicegui-sortable-filtered'}, on_filter=on_filter):
        for i in range(1, 7):
            if i == 4:
                with ui.card().classes('nicegui-sortable-filtered'):
                    ui.label('Filtered').classes('text-red-800')
            else:
                with ui.card():
                    ui.label(f'Item {i}')


@doc.demo('Thresholds', '''
    This example demonstrates how swap thresholds affect drag and drop behavior in sortable lists.
    The threshold determines when items will swap positions as you drag an item over others.
''')
def thresholds_demo() -> None:
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

            with ui.sortable({
                'swapThreshold': 0.5,  # Initial value
                'invertedSwapThreshold': 0.5  # Add this initial value
            }) as vertical_sortable:
                for i in range(1, 5):
                    with ui.card().classes('p-4 m-2 bg-blue-100 dark:bg-blue-800 threshold-card') as card:
                        north_indicator = ui.element('div').classes('swap-zone-indicator north').style(
                            'position: absolute; background-color: rgba(255,0,0,0.2); ' +
                            'width: 100%; left: 0; transition: all 0.3s ease;'
                        )
                        south_indicator = ui.element('div').classes('swap-zone-indicator south').style(
                            'position: absolute; background-color: rgba(255,0,0,0.2); ' +
                            'width: 100%; left: 0; transition: all 0.3s ease;'
                        )

                        vertical_cards.append((north_indicator, south_indicator))
                        ui.label(f'Drag {i}').classes('text-center')

        # Horizontal list panel
        with ui.tab_panel(horizontal_tab):
            # Create a container for horizontal visual indicators
            horizontal_cards = []

            with ui.sortable({
                'direction': 'horizontal',  # Set direction to horizontal
                'swapThreshold': 0.5,
                'invertedSwapThreshold': 0.5
            }).classes('flex-row').style('overflow-y: auto;') as horizontal_sortable:
                for i in range(1, 5):
                    with ui.card().classes(
                        'p-4 m-2 bg-green-100 dark:bg-green-800 horizontal-threshold-card'
                    ):
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
        vertical_sortable.set_option('swapThreshold', threshold_value)
        vertical_sortable.set_option('invertedSwapThreshold', threshold_value)
        vertical_sortable.set_option('invertSwap', invert_value)

        # Update horizontal sortable
        horizontal_sortable.set_option('swapThreshold', threshold_value)
        horizontal_sortable.set_option('invertedSwapThreshold', threshold_value)
        horizontal_sortable.set_option('invertSwap', invert_value)

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

    # Initialize the display
    update_threshold_ui()

    # Add event handlers for UI controls
    swap_threshold.on('update:model-value', update_threshold_ui)
    invert_swap.on('update:model-value', update_threshold_ui)

    # Add supporting CSS
    ui.add_css('''
    .threshold-card {
        position: relative;
        min-height: 80px;
        width: 100%;
    }
    .horizontal-threshold-card {
        position: relative;
    }
    .swap-zone-indicator {
        pointer-events: none;
        z-index: 10;
        border: 2px dashed rgba(255,0,0,0.5);
    }
    ''')


@doc.demo('Grid', '''
    You can create a sortable grid layout with flex wrapping.
''')
def grid_example() -> None:
    with ui.sortable().classes('flex flex-wrap flex-row'):
        for i in range(1, 21):
            with ui.card().classes('grid-square w-20 m-1 p-2 items-center justify-center'):
                ui.label(f'Item {i}')


@doc.demo('Nested Sortables', '''
    This example demonstrates nested sortable lists where items can be dragged between different levels.
''')
def nested_sortables() -> None:
    # Create a helper function to recursively initialize nested sortables
    def create_nested_list(items, level=1):
        with ui.sortable({
            'group': 'nested',
            'fallbackOnBody': True,
            'swapThreshold': 0.4,
            'invertSwap': True,
            'emptyInsertThreshold': 10,
        }).classes(f'nicegui-sortable-nested level-{level}'):
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
                    ]
                },
                {'text': 'Item 2.3'},
            ]
        },
        {'text': 'Item 1.2'},
        {
            'text': 'Item 1.3',
            'children': [
                {'text': 'Item 2.4'},
                {'text': 'Item 2.5'},
            ]
        }
    ]

    with ui.element('div').classes('nested-container'):
        create_nested_list(nested_data)

    # Add improved supporting styles for the nested sortables
    ui.add_css('''
    .nested-item {
        background-color: #2d3748;
        transition: background-color 0.2s;
    }

    .level-1 {
        background-color: #2d3748;
    }

    .level-2 {
        background-color: #1e2a3b;
    }

    .level-3 {
        background-color: #171f2e;
    }

    .nested-item:hover {
        background-color: #3a4a5e;
    }

    .nicegui-sortable-nested:empty {
        background-color: rgba(59, 130, 246, 0.1);
    }

    .nested-children:hover .nicegui-sortable-nested:empty {
        background-color: rgba(59, 130, 246, 0.2);
        border-color: #4b5563;
    }
    ''')


@doc.demo('MultiDrag Plugin', '''
    Hold down Ctrl/Cmd key while selecting items to select multiple. Then drag them as a group.
''')
def multi_drag() -> None:
    with ui.sortable({
        'multiDrag': True,
        'multiDragKey': 'ctrl',
        'multiDragClass': 'nicegui-sortable-multi-selected'
    }, on_select=on_select, on_deselect=on_deselect):
        for i in range(1, 7):
            with ui.card():
                ui.label(f'Item {i} (hold Ctrl/Cmd to select multiple)')


@doc.demo('Swap Plugin', '''
    Items will swap places instead of sorting when dragged over each other.
''')
def swap_plugin() -> None:
    with ui.sortable({
        'swap': True,
        'swapClass': 'nicegui-sortable-swap-highlight'
    }):
        for i in range(1, 7):
            with ui.card():
                ui.label(f'Item {i} (will swap instead of sort)')


@doc.demo('OnSpill Plugins', '''
    These examples demonstrate what happens when items are dragged outside of their containers.
''')
def onspill_plugins() -> None:
    with ui.row():
        with ui.card():
            ui.label('RemoveOnSpill Plugin').classes('text-h6')
            ui.label('Drag an item outside the list to remove it.')

            with ui.sortable({'removeOnSpill': True}, on_spill=on_spill):
                for i in range(1, 7):
                    with ui.card().classes('bg-red-900'):
                        ui.label(f'Drag outside to remove {i}')

        with ui.card():
            ui.label('RevertOnSpill Plugin').classes('text-h6')
            ui.label('Drag an item outside the list and it will revert to original position.')

            with ui.sortable({'revertOnSpill': True}, on_spill=on_spill):
                for i in range(1, 7):
                    with ui.card().classes('bg-green-900'):
                        ui.label(f'Drag outside to revert {i}')


@doc.demo('AutoScroll Plugin', '''
    This example demonstrates auto-scrolling when dragging near the edges of a scrollable container.
''')
def autoscroll_plugin() -> None:
    with ui.element('div').style('max-height: 300px; overflow-y: auto; padding: 10px;'):
        with ui.sortable({
            'autoScroll': True,
            'scrollSensitivity': 20,
            'scrollSpeed': 15
        }):
            for i in range(1, 15):
                with ui.card():
                    ui.label(f'Item {i} (drag up/down to auto-scroll)')


@doc.demo('Dynamic List Management', '''
    This example shows how to dynamically add and remove items from a sortable list.
''')
def dynamic_list_management() -> None:
    def add_deletable_object(label: str, sortable_object: ui.sortable):
        with ui.card() as card:
            with ui.row().classes('items-center w-full'):
                ui.label(label).classes('flex-grow')
                ui.button(
                    icon='delete',
                    color='red',
                    on_click=lambda e: sortable_object.remove_item(card),
                ).classes('min-w-0 w-8 h-8')

    def add_new_item(string: str, sortable_object: ui.sortable):
        with sortable_object:
            add_deletable_object(string, sortable_object)
        ui.notify('Item added to the list')

    with ui.sortable({'fallbackOnBody': True}, on_end=on_end) as dynamic_sortable:
        for i in range(1, 5):
            add_deletable_object(f'Sortable Item {i} - Drag to reorder', dynamic_sortable)

    # Form for adding new items
    with ui.row().classes('w-full items-center mb-4'):
        new_item_input = ui.input('Enter new item text').classes('flex-grow mr-2')
        ui.button(
            'Add Item',
            on_click=lambda: [add_new_item(new_item_input.value, dynamic_sortable), new_item_input.set_value('')],
        ).classes('bg-green-500')

    # Action buttons
    with ui.row().classes('mt-4'):
        ui.button('Delete All', color='red', on_click=dynamic_sortable.clear).classes('mr-2')
        ui.button('Add 3 Random Items', color='green', on_click=lambda: [
            add_new_item(f'Random Item {randint(1, 100)}', dynamic_sortable) for _ in range(3)]).classes('mr-2')

        async def show_current_order():
            items_text = [item.default_slot.children[0].default_slot.children[0].text
                          for item in dynamic_sortable.default_slot.children]
            ui.notify(f'Current order: {items_text}')

        ui.button('Show Current Order', on_click=show_current_order)


doc.reference(ui.sortable)
