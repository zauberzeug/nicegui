from nicegui import ui

from . import doc


@doc.demo(ui.input_chips)
def main_demo() -> None:
    ui.input_chips(value=['default', 'with', 'chips'])


@doc.demo('New value modes', '''
    There are three new value modes: add, add-unique and toggle (default).
    `add` adds all values to the list (allowing duplicates), 'add-unique' adds only unique values to the list, 
    and 'toggle' adds or removes the value (based on if it exists or not in the list).
    If you are updating the values via function, you also need to call `update()` afterwards to let the change take effect.
''')
def new_value_modes():
    import random

    def add_random():
        chips.append_values(str(random.randint(1, 5)))
        chips.update()

    chips = ui.input_chips() \
        .classes('w-64')
    ui.toggle(
        {"add": "add", "add-unique": "add-unique", "toggle": "toggle"},
        value="toggle",
    ).on_value_change(lambda e: chips._props.update({"new-value-mode": e.value}))
    ui.button("Add Random", on_click=add_random)


@doc.demo('Delimit values', '''
    You can delimit values with the help of `on_change`. 
    If you are binding value from `input_chips`, you will need to manually update the bindings on value change.
    Note that, `on_change` is not only limited to `delimiting values` but can be changed as per your needs.

''')
def delimit_values():
    from nicegui import events

    def split_values(e: events.ValueChangeEventArguments):
        new_value = e.sender.get_new_value()
        if new_value is not None and ',' in new_value:
            e.value.remove(new_value)
            e.sender.append_values(new_value.split(','))
        l.text = ', '.join(e.sender.value)

    c = ui.input_chips(on_change=split_values)
    l = ui.label().bind_text_from(c, 'value', backward=', '.join)


doc.reference(ui.input_chips)
