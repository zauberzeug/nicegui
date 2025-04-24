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

    with ui.sortable(on_end=on_end, animation=150, ghost_class='blue-background-class') as simple_sortable:
        for i in range(1, 7):
            with ui.card().classes('p-4 mb-2 list-group-item'):
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
                    with ui.card().classes('p-2 mb-1 list-group-item'):
                        ui.label(f'Item {i}')

        with ui.card().classes('w-64 ml-4'):
            ui.label('List 2').classes('text-h6')
            with ui.sortable(group='shared', animation=150, on_add=on_add, on_sort=on_sort) as list2:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1 list-group-item tinted'):
                        ui.label(f'Item {i}')

# Example 3: Cloning
with ui.card():
    ui.label('Example 3: Cloning').classes('text-h5')
    ui.label('Try dragging from one list to another. The item you drag will be cloned and the clone will stay in the original list.')

    with ui.row():
        with ui.card().classes('w-64'):
            ui.label('List 1 (Clone Source)').classes('text-h6')
            with ui.sortable(group={'name': 'clone-example', 'pull': 'clone'},
                             animation=150) as clone_list1:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1 list-group-item'):
                        ui.label(f'Item {i}')

        with ui.card().classes('w-64 ml-4'):
            ui.label('List 2 (Clone Source)').classes('text-h6')
            with ui.sortable(group={'name': 'clone-example', 'pull': 'clone'},
                             animation=150) as clone_list2:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1 list-group-item tinted'):
                        ui.label(f'Item {i}')

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
                    with ui.card().classes('p-2 mb-1 list-group-item'):
                        ui.label(f'Item {i}')

        with ui.card().classes('w-64 ml-4'):
            ui.label('Sortable List').classes('text-h6')
            with ui.sortable(group='shared-disabled', animation=150) as disabled_sort_list2:
                for i in range(1, 7):
                    with ui.card().classes('p-2 mb-1 list-group-item tinted'):
                        ui.label(f'Item {i}')

# Example 5: Handle Example
with ui.card():
    ui.label('Example 5: Handle').classes('text-h5')
    ui.label('Dragging is only possible using the handle')

    with ui.sortable(handle='.handle', animation=150, on_move=on_move) as handle_sortable:
        for i in range(1, 7):
            with ui.card().classes('p-2 mb-1 list-group-item'):
                with ui.row().classes('items-center w-full'):
                    ui.icon('drag_handle').classes("handle").style("cursor: move;")
                    ui.label(f'Item {i}')

# Example 6: Filter Example
with ui.card():
    ui.label('Example 6: Filter').classes('text-h5')
    ui.label('Try dragging the item with a red background. It cannot be done, because that item is filtered out using the "filter" option.')

    with ui.sortable(filter='.filtered', animation=150, on_filter=on_filter) as filter_sortable:
        for i in range(1, 7):
            if i == 4:
                with ui.card().classes('p-2 mb-1 list-group-item filtered bg-red-200'):
                    ui.label('Filtered').classes('text-red-800')
            else:
                with ui.card().classes('p-2 mb-1 list-group-item'):
                    ui.label(f'Item {i}')

# Example 7: MultiDrag Plugin
with ui.card():
    ui.label('Example 7: MultiDrag Plugin').classes('text-h5')
    ui.label('Hold down Ctrl/Cmd key while selecting items to select multiple. Then drag them as a group.')

    with ui.sortable(
        animation=150,
        multi_drag=True,
        multi_drag_key='ctrl',
        selected_class='multi-selected',
        on_select=on_select,
        on_deselect=on_deselect
    ) as multi_drag_sortable:
        for i in range(1, 7):
            with ui.card().classes('p-2 mb-1 list-group-item'):
                ui.label(f'Item {i} (hold Ctrl/Cmd to select multiple)')

# Example 8: Swap Plugin
with ui.card():
    ui.label('Example 8: Swap Plugin').classes('text-h5')
    ui.label('Items will swap places instead of sorting when dragged over each other.')

    with ui.sortable(
        animation=150,
        swap=True,
        swap_class='swap-highlight'
    ) as swap_sortable:
        for i in range(1, 7):
            with ui.card().classes('p-2 mb-1 list-group-item'):
                ui.label(f'Item {i} (will swap instead of sort)')

# Example 9: OnSpill Plugins - Remove and Revert
with ui.card():
    ui.label('Example 9: OnSpill Plugins').classes('text-h5')
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
                    with ui.card().classes('p-2 mb-1 list-group-item bg-red-100'):
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
                    with ui.card().classes('p-2 mb-1 list-group-item bg-green-100'):
                        ui.label(f'Drag outside to revert {i}')

# Example 10: AutoScroll Plugin
with ui.card():
    ui.label('Example 10: AutoScroll Plugin').classes('text-h5')
    ui.label('This example demonstrates auto-scrolling when dragging near the edges of the container.')

    with ui.element('div').style('max-height: 300px; overflow-y: auto; padding: 10px;'):
        with ui.sortable(
            animation=150,
            auto_scroll=True,
            scroll_sensitivity=20,
            scroll_speed=15
        ) as auto_scroll_sortable:
            for i in range(1, 15):
                with ui.card().classes('p-2 mb-1 list-group-item'):
                    ui.label(f'Item {i} (drag up/down to auto-scroll)')


# Example 11: Add/Remove Items in Sortable List
def add_deletable_object(label: str):
    with ui.card().classes('p-2 mb-1 list-group-item'):
        with ui.row().classes('items-center w-full'):
            ui.label(label).classes('flex-grow')
            ui.button(icon='delete', color='red',
                      on_click=lambda e: e.sender.parent_slot.parent.parent_slot.parent.delete()).classes('min-w-0 w-8 h-8')


def add_new_item(string: str):
    with dynamic_sortable:
        add_deletable_object(string)
    ui.notify('Item added to the list')


with ui.card():
    ui.label('Example 11: Add/Remove Items').classes('text-h5')
    ui.label('This example shows how to dynamically add and remove items from a sortable list.')

    # Form for adding new items
    with ui.row().classes('w-full items-center mb-4'):
        new_item_input = ui.input('Enter new item text').classes('flex-grow mr-2')
        ui.button('Add Item', on_click=lambda: add_new_item(new_item_input.value)).classes('bg-green-500')
        new_item_input.value = ''  # Clear the input

    with ui.sortable(animation=150, on_end=on_end) as dynamic_sortable:
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


# Add CSS for styling
ui.add_head_html("""
<style>
.nicegui-sortable {
    padding: 8px;
    border-radius: 4px;
    background-color: #f5f5f5;
    min-height: 40px;
}

.sortable-ghost {
    opacity: 0.4;
    background-color: #c8ebfb;
}

.sortable-chosen {
    background-color: #e8f4fd;
}

.sortable-drag {
    opacity: 0.8;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
}

.blue-background-class {
    background-color: #c8ebfb;
}

.tinted {
    background-color: #f8d7da;
}

.list-group-item {
    position: relative;
    display: block;
    margin-bottom: -1px;
    background-color: #fff;
    border: 1px solid rgba(0,0,0,.125);
}

.handle {
    cursor: move;
}

.multi-selected {
    background-color: #c8e6fa !important;
    border: 1px solid #0d6efd !important;
}

.swap-highlight {
    background-color: #ffeeba !important;
    border: 1px solid #ffc107 !important;
}

.grid-container {
    width: 100%;
    padding: 10px;
}

.grid-square {
    display: inline-block;
    width: 80px;
    height: 80px;
    margin: 5px;
    text-align: center;
    line-height: 80px;
    background-color: #fff;
    border: 1px solid #ddd;
}

.filtered {
    background-color: #f8d7da !important;
    cursor: not-allowed;
}
</style>
""")

ui.run(title="SortableJS Complete Plugin Examples", native=True)
