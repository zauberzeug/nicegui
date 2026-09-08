from nicegui import ui

from . import doc


@doc.demo(ui.select)
def main_demo() -> None:
    select1 = ui.select([1, 2, 3], value=1)
    select2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')


@doc.demo('Search-as-you-type', '''
    You can activate `with_input` to get a text input with autocompletion.
    The options will be filtered as you type.
''')
def search_as_you_type():
    continents = [
        'Asia',
        'Africa',
        'Antarctica',
        'Europe',
        'Oceania',
        'North America',
        'South America',
    ]
    ui.select(options=continents, with_input=True,
              on_change=lambda e: ui.notify(e.value)).classes('w-40')


@doc.demo('Multi selection', '''
    You can activate `multiple` to allow the selection of more than one item.
''')
def multi_select():
    names = ['Alice', 'Bob', 'Carol']
    ui.select(names, multiple=True, value=names[:2], label='comma-separated') \
        .classes('w-64')
    ui.select(names, multiple=True, value=names[:2], label='with chips') \
        .classes('w-64').props('use-chips')


@doc.demo('Update options', '''
    Options can be changed with the `options` property.
    But then you also need to call `update()` afterwards to let the change take effect.
    `set_options` is a shortcut that does both and works well for lambdas.
''')
def update_selection():
    select = ui.select([1, 2, 3], value=1)
    with ui.row():
        ui.button('4, 5, 6', on_click=lambda: select.set_options([4, 5, 6], value=4))
        ui.button('1, 2, 3', on_click=lambda: select.set_options([1, 2, 3], value=1))


@doc.demo('Rich options', '''
    Options are not limited to scalars.
    A list may hold dataclasses or dictionaries, and then `value` is the selected option itself.
    Use `option_label` to say how an option should be labelled.

    A rich option's own fields are sent to the client,
    so slots can access them as `props.opt.<key>`.
    The keys "value" and "label" are reserved.

    The element is generic in its option type,
    so a type checker knows that `person` is a `Person` and that `select.value` is a `Person | None`
    (a `list[Person]` if `multiple` is True).
''')
def rich_options():
    from dataclasses import dataclass

    @dataclass
    class Person:
        name: str
        icon: str
        team: str

    people = [
        Person('Alice', 'engineering', 'Engineering'),
        Person('Bob', 'palette', 'Design'),
        Person('Carol', 'query_stats', 'Data Science'),
    ]
    select = ui.select(people, value=people[0], option_label=lambda person: person.name) \
        .classes('w-64')
    select.add_slot('option', '''
        <q-item v-bind="props.itemProps">
            <q-item-section avatar>
                <q-icon :name="props.opt.icon" />
            </q-item-section>
            <q-item-section>
                <q-item-label>{{ props.opt.label }}</q-item-label>
                <q-item-label caption>{{ props.opt.team }}</q-item-label>
            </q-item-section>
        </q-item>
    ''')
    ui.label().bind_text_from(select, 'value', lambda person: f'Selected: {person.name}')


doc.reference(ui.select)
