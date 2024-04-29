from nicegui import ui

from . import doc


@doc.demo(ui.chip)
def main_demo() -> None:
    with ui.row().classes('gap-1'):
        ui.chip('Click me', icon='ads_click', on_click=lambda: ui.notify('Clicked'))
        ui.chip('Selectable', selectable=True, icon='bookmark', color='orange')
        ui.chip('Removable', removable=True, icon='label', color='indigo-3')
        ui.chip('Styled', icon='star', color='green').props('outline square')
        ui.chip('Disabled', icon='block', color='red').set_enabled(False)


@doc.demo('Dynamic chip elements as labels/tags', '''
    This demo shows how to implement a dynamic list of chips as labels or tags.
    You can add new chips by typing a label and pressing Enter or pressing the plus button.
    Removed chips still exist, but their value is set to `False`.
''')
def labels():
    def add_chip():
        with chips:
            ui.chip(label_input.value, icon='label', color='silver', removable=True)
        label_input.value = ''

    label_input = ui.input('Add label').on('keydown.enter', add_chip)
    with label_input.add_slot('append'):
        ui.button(icon='add', on_click=add_chip).props('round dense flat')

    with ui.row().classes('gap-0') as chips:
        ui.chip('Label 1', icon='label', color='silver', removable=True)

    ui.button('Restore removed chips', icon='unarchive',
              on_click=lambda: [chip.set_value(True) for chip in chips]) \
        .props('flat')


doc.reference(ui.chip)
