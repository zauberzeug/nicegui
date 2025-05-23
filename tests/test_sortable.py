from nicegui import ui
from nicegui.testing import Screen


def test_sortable_renders(screen: Screen):
    """Test if the sortable element renders correctly."""
    @ui.page('/')
    def page():
        with ui.sortable():
            ui.label('Item 1')
            ui.label('Item 2')
            ui.label('Item 3')

    screen.open('/')

    screen.should_contain('Item 1')
    screen.should_contain('Item 2')
    screen.should_contain('Item 3')

    element = screen.find_by_class('nicegui-sortable')
    assert element is not None


def test_sortable_options(screen: Screen):
    """Test if sortable options are properly set."""
    options = {
        'disabled': True,
        'animation': 200,
        'handle': '.handle',
        'filter': '.filtered'
    }

    @ui.page('/')
    def page():
        nonlocal options
        with ui.sortable(options) as sortable:
            ui.label('Item 1')
            ui.label('Item 2').classes('filtered')
            with ui.row():
                ui.icon('drag_handle').classes('handle')
                ui.label('Item 3')

            ui.button('Check Options', on_click=lambda: ui.notify(
                f"Animation: {sortable._props['options']['animation']}, "
                f"Handle: {sortable._props['options']['handle']}, "
                f"Filter: {sortable._props['options']['filter']}, "
                f"Disabled: {sortable._props['options']['disabled']}"
            ))

    screen.open('/')

    screen.click('Check Options')
    screen.should_contain('Animation: 200')
    screen.should_contain('Handle: .handle')
    screen.should_contain('Filter: .filtered')
    screen.should_contain('Disabled: True')


def test_sortable_synchronization(screen: Screen):
    """Test if the sortable synchronizes the Python side when items are reordered."""
    @ui.page('/')
    def page():
        with ui.sortable() as sortable:
            ui.label('Item 1')
            ui.label('Item 2')
            ui.label('Item 3')

            def show_order():
                current_order = ', '.join(item.text for item in sortable.default_slot.children)
                ui.notify(f'Current order: {current_order}')

        ui.button('Show Order', on_click=show_order)
        ui.button('Reverse Order', on_click=lambda: sortable.sort(
            list(reversed(sortable.default_slot.children)), True))

    screen.open('/')

    screen.click('Show Order')
    screen.should_contain('Current order: Item 1, Item 2, Item 3')

    screen.click('Reverse Order')

    screen.click('Show Order')
    screen.should_contain('Current order: Item 3, Item 2, Item 1')


def test_sortable_drag_and_drop(screen: Screen):
    """Test dragging and dropping items within a sortable container."""
    @ui.page('/')
    def page():
        with ui.sortable() as sortable:
            ui.label('Item 1').classes('draggable')
            ui.label('Item 2').classes('draggable')
            ui.label('Item 3').classes('draggable')

            def show_order():
                current_order = ', '.join(item.text for item in sortable.default_slot.children)
                ui.notify(f'Current order: {current_order}')

        ui.button('Show Order', on_click=show_order)

    screen.open('/')

    screen.click('Show Order')
    screen.should_contain('Current order: Item 1, Item 2, Item 3')

    screen.drag_and_drop('Item 1', 'Item 3')

    # Wait for the sorting to complete
    screen.wait(0.5)

    screen.click('Show Order')
    screen.should_contain('Current order: Item 2, Item 3, Item 1')


def test_sortable_drag_between_containers(screen: Screen):
    """Test dragging items between two different sortable containers."""

    src1, src2, src3 = None, None, None
    target1, target2, target3 = None, None, None

    @ui.page('/')
    def page():
        nonlocal src1, src2, src3, target1, target2, target3
        ui.label('Source List').classes('text-xl')
        with ui.sortable({'group': 'shared-group'}) as source_sortable:
            src1 = ui.label('Source Item 1').classes('draggable bg-blue-100')
            src2 = ui.label('Source Item 2').classes('draggable bg-blue-100')
            src3 = ui.label('Source Item 3').classes('draggable bg-blue-100')

            def show_source_order():
                current_order = ', '.join(item.text for item in source_sortable.default_slot.children)
                ui.notify(f'Source order: {current_order}')

        ui.label('Target List').classes('text-xl mt-4')
        with ui.sortable({'group': 'shared-group'}) as target_sortable:
            target1 = ui.label('Target Item A').classes('draggable bg-green-100')
            target2 = ui.label('Target Item B').classes('draggable bg-green-100')
            target3 = ui.label('Target Item C').classes('draggable bg-green-100')

            def show_target_order():
                current_order = ', '.join(item.text for item in target_sortable.default_slot.children)
                ui.notify(f'Target order: {current_order}')

        with ui.column():
            ui.button('Show Source Order', on_click=show_source_order)
            ui.button('Show Target Order', on_click=show_target_order)

    screen.open('/')

    screen.click('Show Source Order')
    screen.should_contain('Source order: Source Item 1, Source Item 2, Source Item 3')

    screen.click('Show Target Order')
    screen.should_contain('Target order: Target Item A, Target Item B, Target Item C')

    screen.drag_and_drop('Source Item 2', 'Target Item B')

    # Wait for the sorting to complete
    screen.wait(0.5)

    screen.click('Show Source Order')
    screen.should_contain('Source order: Source Item 1, Source Item 3')

    screen.click('Show Target Order')
    screen.should_contain('Target order: Target Item A, Source Item 2, Target Item B, Target Item C')
