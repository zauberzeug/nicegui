from nicegui import ui

from . import doc


@doc.demo(ui.chip)
def main_demo() -> None:
    with ui.row().classes('gap-1'):
        ui.chip('Click me', icon='ads_click', on_click=lambda: ui.notify('Clicked'))
        ui.chip('Selectable', selectable=True, icon='bookmark',
                color='orange').on_selection_change(lambda e: ui.notify(e.sender.selected))
        ui.chip('Removable', removable=True, icon='label', color='indigo')
        ui.chip('Styled', icon='star', color='green').props('outline square')
        ui.chip('Disabled', icon='block', color='red').set_enabled(False)


@doc.demo('Dynamic chip elements as labels/tags', '''
    This demo shows how to implement a dynamic list of chips as labels or tags.
    You can add new chips by typing a label and pressing Enter or pressing the plus button.
    Removed chips still exist, but their value is set to False.
''')
def labels():
    def on_chip_change():
        ui.notify('Labels: ' + ', '.join(chip.text for chip in label_chips.default_slot.children if chip.value))

    def add_chip():
        if not (val := label.value.strip()):
            return
        with label_chips:
            ui.chip(val, icon='label', color='gray', removable=True, on_value_change=on_chip_change)
            on_chip_change()
        label.value = ''

    with ui.input('Add label', on_enter=add_chip).props('filled') as label:
        with label.add_slot('prepend'):
            ui.icon('label', color='primary')
        with label.add_slot('append'):
            ui.button(icon='add', on_click=add_chip).props('round dense flat')

    with ui.row().classes('gap-0') as label_chips:
        ui.chip('Label 1', icon='label', color='gray', removable=True, on_value_change=on_chip_change)

    ui.button('Restore', on_click=lambda: [chip.set_value(True) for chip in label_chips.default_slot.children])


doc.reference(ui.chip)
