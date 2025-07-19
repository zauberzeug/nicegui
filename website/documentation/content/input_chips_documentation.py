from nicegui import ui

from . import doc


@doc.demo(ui.input_chips)
def main_demo() -> None:
    ui.input_chips(value=['default', 'with', 'chips'])


@doc.demo('New value modes', '''
    There are three new value modes: add, add-unique and toggle (default).
    `add` adds all values to the list (allowing duplicates), 'add-unique' adds only unique values to the list,
    and 'toggle' adds or removes the value (based on if it exists or not in the list).
''')
def new_value_modes():
    chips = ui.input_chips() \
        .classes('w-64')
    ui.toggle(
        {'add': 'add', 'add-unique': 'add-unique', 'toggle': 'toggle'},
        value='toggle',
    ).on_value_change(lambda e: chips.props.update({'new-value-mode': e.value}))


@doc.demo('Delimit values', '''
    You can delimit values with the help of `on_change`.
    Note that, `on_change` is not only limited to `delimiting values` but can be modified as per your needs.
''')
def delimit_values():
    from nicegui import events

    def split_values(e: events.ValueChangeEventArguments):
        for value in e.value[:]:
            if ',' in value:
                e.value.remove(value)
                e.sender.value = e.value + value.split(',')

    c = ui.input_chips(on_change=split_values)
    ui.label().bind_text_from(c, 'value', backward=', '.join)


doc.reference(ui.input_chips)
