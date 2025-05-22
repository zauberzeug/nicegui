from nicegui import ui
from random import randint

from . import doc


# Event handlers
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
        ui.button('Enable', on_click=lambda: simple_sortable.enable())
        ui.button('Disable', on_click=lambda: simple_sortable.disable())
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
    NOTE: The python object gets moved to the cloned object in the DOM. The original object loses its python object reference.
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
            label="Slider",
            bg="",
        ):
            super().__init__()
            self.label = label
            self.bg = bg

            # Create a new card with the same content but possibly different styling
            with self.classes(f'{self.bg}'):
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
                    ClonableCard(f'Item {i}', "bg-amber-500")


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
                    ui.icon('drag_handle').classes("nicegui-sortable-handle")
                    ui.label(f'Item {i}')


@doc.demo('Filter', '''
    You can prevent specific items from being draggable by applying a filter.
''')
def filter_example() -> None:
    with ui.sortable({'filter': '.nicegui-sortable-filtered'}, on_filter=on_filter):
        for i in range(1, 7):
            if i == 4:
                with ui.card().classes('nicegui-sortable-filtered bg-red-200'):
                    ui.label('Filtered').classes('text-red-800')
            else:
                with ui.card():
                    ui.label(f'Item {i}')


@doc.demo('Grid', '''
    You can create a sortable grid layout with flex wrapping.
''')
def grid_example() -> None:
    with ui.sortable({
        'delay': 150  # Adding a small delay helps with touch devices
    }).classes('flex flex-wrap flex-row'):
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
            'delay': 150
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
    ui.add_css("""
    /* Basic styling for nested items */
    .nested-item {
        background-color: #2d3748;
        transition: background-color 0.2s;
    }

    /* Color differentiation by nesting level */
    .level-1 {
        background-color: #2d3748;
    }

    .level-2 {
        background-color: #1e2a3b;
    }

    .level-3 {
        background-color: #171f2e;
    }

    /* Hover effect */
    .nested-item:hover {
        background-color: #3a4a5e;
    }

    /* Empty sortable containers styling */
    .nicegui-sortable-nested:empty {
        background-color: rgba(59, 130, 246, 0.1);
    }

    /* Highlight empty containers on hover for better UX */
    .nested-children:hover .nicegui-sortable-nested:empty {
        background-color: rgba(59, 130, 246, 0.2);
        border-color: #4b5563;
    }
    """)


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
    def add_deletable_object(label: str):
        with ui.card():
            with ui.row().classes('items-center w-full'):
                ui.label(label).classes('flex-grow')
                ui.button(icon='delete', color='red',
                          on_click=lambda e: e.sender.parent_slot.parent.parent_slot.parent.delete()).classes('min-w-0 w-8 h-8')

    def add_new_item(string: str):
        with dynamic_sortable:
            add_deletable_object(string)
        ui.notify('Item added to the list')

    # Form for adding new items
    with ui.row().classes('w-full items-center mb-4'):
        new_item_input = ui.input('Enter new item text').classes('flex-grow mr-2')
        ui.button('Add Item', on_click=lambda: add_new_item(new_item_input.value)).classes('bg-green-500')
        new_item_input.value = ''  # Clear the input

    with ui.sortable({'fallbackOnBody': True}, on_end=on_end) as dynamic_sortable:
        # Pre-populate with some items
        for i in range(1, 5):
            add_deletable_object(f'Sortable Item {i} - Drag to reorder')

    # Action buttons
    with ui.row().classes('mt-4'):
        ui.button('Delete All', color='red', on_click=lambda: dynamic_sortable.clear()).classes('mr-2')
        ui.button('Add 3 Items', color='green', on_click=lambda: [
            add_new_item(f'Random Item {randint(1, 100)}') for _ in range(3)]).classes('mr-2')

        async def show_current_order():
            items_text = [item.default_slot.children[0].default_slot.children[0].text
                          for item in dynamic_sortable.default_slot.children]
            ui.notify(f'Current order: {items_text}')

        ui.button('Show Current Order', on_click=show_current_order)


doc.reference(ui.sortable)
