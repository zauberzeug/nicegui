from nicegui import ui

from . import doc


@doc.demo(ui.fab)
def main_demo() -> None:
    with ui.fab(icon='add', label='Add Item', color='green-5') as fab:
        ui.fab_action(icon='train', text='Train', color='green-5').on('click', lambda: ui.notify('train'))
        ui.fab_action(icon='sailing', text='Boat', color='green-5').on('click', lambda: ui.notify('boat'))
        ui.fab_action(icon='rocket', text='Rocket', color='green-5').on('click', lambda: ui.notify('rocket'))


@doc.demo('Migrating to the new implementation', '''
    Here is an example of two identical FABs, one using the old implementation using `ui.element`, and one using the new `ui.fab` and `ui.fab_action` elements.

    It is recommended to migrate to the new implementation because:

    - it is more readable and easier to use
    - it is more consistent with other NiceGUI elements
    - it is more performant, as it does not require a server round-trip to open/close the FAB

    The old implementation will remain working, since `ui.element` remains available, but it is not recommended to use it for new code.
''')
def migration_demo() -> None:
    ui.label('Old implementation using ui.element').classes('text-h6')
    with ui.element('q-fab').props('icon=navigation color=green'):
        ui.element('q-fab-action').props('icon=train color=green-5') \
            .on('click', lambda: ui.notify('train'))
        ui.element('q-fab-action').props('icon=sailing color=green-5') \
            .on('click', lambda: ui.notify('boat'))
        ui.element('q-fab-action').props('icon=rocket color=green-5') \
            .on('click', lambda: ui.notify('rocket'))

    ui.label('New implementation using ui.fab and ui.fab_action').classes('text-h6')
    with ui.fab(icon='navigation', color='green'):
        ui.fab_action(icon='train', color='green-5').on('click', lambda: ui.notify('train'))
        ui.fab_action(icon='sailing', color='green-5').on('click', lambda: ui.notify('boat'))
        ui.fab_action(icon='rocket', color='green-5').on('click', lambda: ui.notify('rocket'))


doc.reference(ui.fab, title='Reference for ui.fab')
doc.reference(ui.fab_action, title='Reference for ui.fab_action')
