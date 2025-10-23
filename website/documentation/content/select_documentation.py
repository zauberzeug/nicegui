from nicegui import ui
from nicegui.elements.select import Select

from . import doc


@doc.demo(Select)
def main_demo() -> None:
    select1 = ui.select([1, 2, 3], value=1)
    options = [ui.option(l, v) for v, l in {1: 'One', 2: 'Two', 3: 'Three'}.items()]
    select2 = ui.select(options).bind_value(select1, 'value')


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
    ui.select(names, value=tuple(names[:2]), label='comma-separated') \
        .classes('w-64')
    ui.select(names, value=tuple(names[:2]), label='with chips') \
        .classes('w-64').props('use-chips')


@doc.demo('Update options', '''
    Options can be changed with the `options` property.
    But then you also need to call `update()` afterwards to let the change take effect.
    `set_options` is a shortcut that does both and works well for lambdas.
''')
def update_selection():
    select = ui.select([1, 2, 3], value=1)
    with ui.row():
        ui.button('4, 5, 6', on_click=lambda: select.set_options(map(ui.to_option, [4, 5, 6]), value=ui.to_option(4)))
        ui.button('1, 2, 3', on_click=lambda: select.set_options(map(ui.to_option, [1, 2, 3]), value=ui.to_option(1)))


@doc.demo('Extending options and custom slotting', '''
    Options can be extended by defining our own `Option` `dataclass`.
    In the example below, we define a new `Person` option with additional fields utilized
    in the `option` slot.
''')
def extending_options_and_custom_slotting():
    from dataclasses import dataclass

    @dataclass
    class Person(ui.option[str, int]):
        icon: str
        caption: str

        def __repr__(self) -> str:
            return f"Person({self.label}, {self.value})"

    select_people = (
        ui.select(
            options=[
                Person(
                    label='Joe', value=0, icon='person', 
                    caption='Company: Trilliant Health'
                    ),
                Person(
                    label='Rodja', value=1, icon='person', 
                    caption='Company: Zauberzeug GmbH'
                    ),
                Person(
                    label='Darth Vader', value=2, icon='person_off', 
                    caption='Fired for being evil'
                    ),
            ],
            on_change=lambda e: ui.notify(e.value),
            value=(),
        )
        .props('use-chips')
        .classes('w-64')
    )
    select_people.add_slot(
        'option',
        r'''
        <q-item
            v-bind="props.itemProps"
        >
            <q-item-section avatar>
                <q-icon :name="props.opt.icon"></ion-icon>
            </q-item-section>
            <q-item-section>
                <q-item-label>{{ props.opt.label }}</q-item-label>
                <q-item-label caption>{{ props.opt.caption }}</q-item-label>
            </q-item-section>
        </q-item>
        '''
    )


doc.reference(Select)
