from nicegui import ui

from . import doc


@doc.demo('Sortable', '''
    Container elements like `ui.column`, `ui.row`, and `ui.card` can be made sortable
    via drag-and-drop using the `make_sortable()` method.
    It returns a `Sortable` controller for enabling, disabling, or destroying the sort behavior.
''')
def main_demo() -> None:
    with ui.column() as column:
        for name in ['Alice', 'Bob', 'Carol']:
            with ui.card().classes('w-full p-2'):
                ui.label(name)
    column.make_sortable(on_end=lambda e: ui.notify(f'Moved from {e.old_index} to {e.new_index}'))


@doc.demo('Cross-Container Dragging', '''
    Use the `group` parameter to allow dragging items between multiple containers.
    All containers with the same group name can exchange items.
''')
def cross_container() -> None:
    with ui.row():
        with ui.column().classes('border p-4') as col1:
            ui.label('Column 1').classes('font-bold')
            for name in ['Alice', 'Bob']:
                with ui.card().classes('w-full p-2'):
                    ui.label(name)
        with ui.column().classes('border p-4') as col2:
            ui.label('Column 2').classes('font-bold')
            for name in ['Carol', 'Dave']:
                with ui.card().classes('w-full p-2'):
                    ui.label(name)
    col1.make_sortable(group='shared')
    col2.make_sortable(group='shared')


@doc.demo('Drag Handle', '''
    Use the `handle` parameter with a CSS selector to restrict dragging to a specific element.
    Only the handle element can initiate a drag operation.
''')
def drag_handle() -> None:
    with ui.column() as column:
        for name in ['Alice', 'Bob', 'Carol']:
            with ui.row().classes('items-center w-full'):
                ui.icon('drag_indicator').classes('handle cursor-move text-gray-400')
                ui.label(name)
    column.make_sortable(handle='.handle')


@doc.demo('Enable / Disable', '''
    The `Sortable` controller returned by `make_sortable()` provides
    `enable()` and `disable()` methods to toggle sorting at runtime.
''')
def enable_disable() -> None:
    with ui.column() as column:
        for name in ['Alice', 'Bob', 'Carol']:
            with ui.card().classes('w-full p-2'):
                ui.label(name)
    sortable = column.make_sortable()
    with ui.row():
        ui.button('Disable', on_click=sortable.disable)
        ui.button('Enable', on_click=sortable.enable)
