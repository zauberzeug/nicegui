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


@doc.demo('Delimit value', '''
    You can activate `use_delimiter` when `new_value_mode` is set as `add` or `add-unique` to add multiple values at once. 
    The values are delimited by `,`, `;`, `|`, `、`, `،`.
''')
def update_selection():
    ui.label("Try adding 'one, two, one'")
    ui.select([],label="Allows all values", new_value_mode="add", use_delimiter=True) \
        .classes('w-64').props('use-chips')
    ui.select([],label="Allows unique values", new_value_mode="add-unique", use_delimiter=True) \
        .classes('w-64').props('use-chips')


doc.reference(ui.select)
