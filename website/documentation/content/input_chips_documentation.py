from nicegui import ui

from . import doc


@doc.demo(ui.input_chips)
def main_demo() -> None:
    ui.input_chips('My favorite chips', value=['Pringles', 'Doritos', "Lay's"])


@doc.demo('New-value modes', '''
    There are three new-value modes: "add", "add-unique", and "toggle" (the default).

    - "add" adds all values to the list (allowing duplicates).
    - "add-unique" adds only unique values to the list.
    - "toggle" adds or removes the value (based on if it exists or not in the list).
''')
def new_value_modes():
    ui.input_chips('Add', new_value_mode='add')
    ui.input_chips('Add unique', new_value_mode='add-unique')
    ui.input_chips('Toggle', new_value_mode='toggle')


@doc.demo('Auto-split values', '''
    This demo shows how to automatically split values when the user enters comma-separated values.
''')
def delimit_values():
    from nicegui import events

    def split_values(e: events.ValueChangeEventArguments):
        for value in e.value[:]:
            e.value.remove(value)
            e.value.extend(value.split(','))

    ui.input_chips(on_change=split_values)
    ui.label('Try entering "x,y,z"!')


doc.reference(ui.input_chips)
