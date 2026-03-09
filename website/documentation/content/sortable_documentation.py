from nicegui import ui

from . import doc


@doc.demo('Sortable', '''
    Container elements like `ui.column`, `ui.row`, and `ui.card` can be made sortable via drag-and-drop
    using the `make_sortable()` method.
    It returns a `Sortable` controller for enabling, disabling, or changing the sort behavior.
''')
def main_demo() -> None:
    with ui.card() as card:
        for name in ['Alice', 'Bob', 'Carol']:
            ui.label(name).classes('cursor-pointer')
    card.make_sortable(on_end=lambda e: ui.notify(f'Moved from {e.old_index} to {e.new_index}'))


@doc.demo('Cross-Container Dragging', '''
    Use the `group` parameter to allow dragging items between multiple containers.
    All containers with the same group name can exchange items.
''')
def cross_container() -> None:
    with ui.row():
        with ui.card() as card1:
            ui.label('Card 1').classes('font-bold')
            for name in ['Alice', 'Bob', 'Carol']:
                ui.label(name).classes('cursor-pointer')
        with ui.card() as card2:
            ui.label('Card 2').classes('font-bold')
            for name in ['Dave', 'Eve', 'Frank']:
                ui.label(name).classes('cursor-pointer')
    card1.make_sortable(group='shared')
    card2.make_sortable(group='shared')


@doc.demo('Drag Handle', '''
    Use the `handle` parameter with a CSS selector to restrict dragging to a specific element.
    Only the handle element can initiate a drag operation.
''')
def drag_handle() -> None:
    with ui.card() as card:
        for name in ['Alice', 'Bob', 'Carol']:
            with ui.row().classes('items-center gap-2'):
                ui.icon('drag_indicator').classes('handle cursor-pointer')
                ui.label(name)
    card.make_sortable(handle='.handle')


@doc.demo('Enable / Disable', '''
    The `Sortable` controller returned by `make_sortable()` provides `enable()` and `disable()` methods to toggle
    sorting at runtime.
''')
def enable_disable() -> None:
    with ui.card() as card:
        for name in ['Alice', 'Bob', 'Carol']:
            ui.label(name).classes('cursor-pointer')
    sortable = card.make_sortable()
    ui.switch('Enable', value=True,
              on_change=lambda e: sortable.enable() if e.value else sortable.disable())
