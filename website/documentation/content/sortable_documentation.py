from nicegui import ui
from nicegui.events import GenericEventArguments

from random import randint

from . import doc


# Event handlers
def on_end(e: GenericEventArguments):
    ui.notify(f'Item moved from {e.args["oldIndex"]} to {e.args["newIndex"]}')


def on_add():
    ui.notify('Item added from another list')


def on_change():
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


@doc.demo('Shared Lists', '''
    You can enable drag and drop between multiple sortable lists by assigning them to the same group.
''')
def shared_lists() -> None:
    with ui.row():
        with ui.card():
            ui.label('List 1').classes('text-h6')
            with ui.sortable({'group': 'shared'}, on_add=on_add, on_change=on_change):
                for i in range(1, 7):
                    with ui.card():
                        ui.label(f'Item {i}')

        with ui.card():
            ui.label('List 2').classes('text-h6')
            with ui.sortable({'group': 'shared'}, on_add=on_add, on_change=on_change):
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

    def handle_true_clone(e):
        # Get info about the added item
        html_id = e.args.get('sourceItem')
        target_index = e.args.get('newIndex')

        # Find the original item in the source list
        # This is where we need to know which list the item came from
        if e.sender.id == true_clone_list1.id:
            source_list = true_clone_list1
            dest_list = true_clone_list2
        else:
            source_list = true_clone_list2
            dest_list = true_clone_list1

        # Find the source element by its ID
        source_element = source_list.get_child_by_id(html_id)

        if source_element:
            with dest_list:
                # Create a clone
                clone = source_element.clone()
                clone.move(dest_list, target_index=target_index)
                # Notify user
                ui.notify(f'Cloned {source_element.label} to position {target_index}')

    with ui.row():
        with ui.card():
            ui.label('List 1').classes('text-h6')
            with ui.sortable({
                'group': {'name': 'true-clone-example', 'pull': 'clone'},
                'cancelClone': True
            }, on_cancel_clone=handle_true_clone) as true_clone_list1:
                for i in range(1, 7):
                    ClonableCard(f'List1 {i}')

        with ui.card():
            ui.label('List 2').classes('text-h6')
            with ui.sortable({
                'group': {'name': 'true-clone-example', 'pull': 'clone'},
                'cancelClone': True
            }, on_cancel_clone=handle_true_clone) as true_clone_list2:
                for i in range(1, 7):
                    ClonableCard(f'List2 {i}', 'bg-amber-500')

        async def show_current_order1():
            items_text = [item.id
                          for item in true_clone_list1.default_slot.children]
            ui.notify(f'Current order: {items_text}')
            dom_order = await true_clone_list1.run_method('getChildrenOrder')
            ui.notify(f'Current DOM order: {dom_order}')

        async def show_current_order2():
            items_text = [item.id
                          for item in true_clone_list2.default_slot.children]
            ui.notify(f'Current order: {items_text}')
            dom_order = await true_clone_list2.run_method('getChildrenOrder')
            ui.notify(f'Current DOM order: {dom_order}')

        ui.button('Show Current Order 1', on_click=show_current_order1)
        ui.button('Show Current Order 2', on_click=show_current_order2)


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


@doc.demo('Event Debugging', '''
    This example shows all available events from SortableJS and displays
    information about them when they're triggered.
''')
def event_debugging() -> None:
    ui.markdown('''
        This demo shows all available sortable events. Try:

        - Use the handle to move items in List 2
        - Dragging items between lists
        - Clicking the filtered (red) item
        - Holding Ctrl/Cmd and clicking multiple items
        - Rearranging items within a list
    ''').classes('mt-4 text-sm')

    # Create a log panel to display event information
    log_panel = ui.log().classes('w-full h-64 overflow-auto bg-gray-800 text-white p-2')

    def log_event(name: str, e: GenericEventArguments):
        '''Log an event to the panel with its name and arguments'''
        log_panel.push(f'{name}: {e.args}')

    # Create handlers for all events
    def on_choose(e: GenericEventArguments): log_event('choose', e)
    def on_unchoose(e: GenericEventArguments): log_event('unchoose', e)
    def on_start(e: GenericEventArguments): log_event('start', e)
    def on_end(e: GenericEventArguments): log_event('end', e)
    def on_add(e: GenericEventArguments): log_event('add', e)
    def on_update(e: GenericEventArguments): log_event('update', e)
    def on_remove(e: GenericEventArguments): log_event('remove', e)
    def on_move(e: GenericEventArguments): log_event('move', e)
    def on_clone(e: GenericEventArguments): log_event('clone', e)
    def on_change(e: GenericEventArguments): log_event('change', e)
    def on_filter(e: GenericEventArguments): log_event('filter', e)
    def on_spill(e: GenericEventArguments): log_event('spill', e)
    def on_select(e: GenericEventArguments): log_event('select', e)
    def on_deselect(e: GenericEventArguments): log_event('deselect', e)

    # Clear the log
    ui.button('Clear Log', on_click=lambda: log_panel.clear()).classes('mb-4')

    def add_remove_handle(e: GenericEventArguments):
        # If moved within its own list, ignore
        if e.args['from'] == e.args['to']:
            return

        if e.args['to'] == sortable2.html_id:  # Add handle
            element = sortable2.get_child_by_id(e.args['item'])
            if element is None:
                assert 'Element should not be None'
                return

            with element.default_slot.children[0].default_slot:
                ui.icon('drag_handle').classes('nicegui-sortable-handle')
            # Reverse to have the handle first
            element.default_slot.children[0].default_slot.children.reverse()
        else:  # Remove handle
            element = sortable1.get_child_by_id(e.args['item'])
            if element is None:
                assert 'Element should not be None'
                return

            element.default_slot.children[0].remove(element.default_slot.children[0].default_slot.children[0])

    with ui.row():
        with ui.card():
            ui.label('List 1').classes('text-h6')
            with ui.sortable({
                'group': {'name': 'event-debugging'},
                'filter': '.nicegui-sortable-filtered',  # Items with this class won't be draggable
                'multiDrag': True,  # Enable multiple selection with Ctrl/Cmd
                'multiDragKey': 'ctrl',
            },
                    on_end=on_end,
                    on_add=on_add,
                    on_change=on_change,
                    on_filter=on_filter,
                    on_spill=on_spill,
                    on_select=on_select,
                    on_deselect=on_deselect) as sortable1:
                for i in range(1, 6):
                    # Make one item non-draggable to test filtering
                    if i == 3:
                        with ui.card().classes('nicegui-sortable-filtered'):
                            ui.label(f'Filtered Item {i} (non-draggable)')
                    else:
                        with ui.card():
                            with ui.row().classes('flex flex-row flex-nowrap items-center'):
                                ui.label(f'Item {i} (hold Ctrl/Cmd to select multiple)')
            sortable1.on('sort_end', add_remove_handle)
            sortable1.on('sort_choose', on_choose)
            sortable1.on('sort_unchoose', on_unchoose)
            sortable1.on('sort_start', on_start)
            sortable1.on('sort_update', on_update)
            sortable1.on('sort_remove', on_remove)
            sortable1.on('sort_move', on_move)
            sortable1.on('sort_clone', on_clone)
            sortable1.on('sort_change', on_change)

        with ui.card():
            ui.label('List 2').classes('text-h6')
            with ui.sortable({
                'handle': '.nicegui-sortable-handle',
                'group': {'name': 'event-debugging'},
            },
                    on_end=on_end,
                    on_add=on_add,
                    on_change=on_change,
                    on_filter=on_filter,
                    on_spill=on_spill,
                    on_select=on_select,
                    on_deselect=on_deselect) as sortable2:
                for i in range(1, 4):
                    with ui.card():
                        with ui.row().classes('flex flex-row flex-nowrap items-center'):
                            ui.icon('drag_handle').classes('nicegui-sortable-handle')
                            ui.label(f'Item {i}')
            sortable2.on('sort_end', add_remove_handle)
            sortable2.on('sort_choose', on_choose)
            sortable2.on('sort_unchoose', on_unchoose)
            sortable2.on('sort_start', on_start)
            sortable2.on('sort_update', on_update)
            sortable2.on('sort_remove', on_remove)
            sortable2.on('sort_move', on_move)
            sortable2.on('sort_clone', on_clone)
            sortable2.on('sort_change', on_change)


doc.reference(ui.sortable)
