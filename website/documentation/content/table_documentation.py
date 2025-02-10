from nicegui import ui

from . import doc


@doc.demo(ui.table)
def main_demo() -> None:
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
        {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
    ]
    rows = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol'},
    ]
    ui.table(columns=columns, rows=rows, row_key='name')


@doc.demo('Omitting columns', '''
    If you omit the `columns` parameter, the table will automatically generate columns from the first row.
    Labels are uppercased and sorting is enabled.

    *Updated in version 2.0.0: The `columns` parameter became optional.*
''')
def omitting_columns():
    ui.table(rows=[
        {'make': 'Toyota', 'model': 'Celica', 'price': 35000},
        {'make': 'Ford', 'model': 'Mondeo', 'price': 32000},
        {'make': 'Porsche', 'model': 'Boxster', 'price': 72000},
    ])


@doc.demo('Default column parameters', '''
    You can define default column parameters that apply to all columns.
    In this example, all columns are left-aligned by default and have a blue uppercase header.

    *Added in version 2.0.0*
''')
def default_column_parameters():
    ui.table(rows=[
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
    ], columns=[
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ], column_defaults={
        'align': 'left',
        'headerClasses': 'uppercase text-primary',
    })


@doc.demo('Selection', '''
    You can set the selection type of a table using the `selection` parameter.
    The `on_select` event handler is called when the selection changes
    and the `selected` property contains the selected rows.

    *Added in version 2.11.0:*
    The `selection` property and the `set_selection` method can be used to change the selection type.
''')
def selection():
    table = ui.table(
        columns=[{'name': 'name', 'label': 'Name', 'field': 'name'}],
        rows=[{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Charlie'}],
        row_key='name',
        on_select=lambda e: ui.notify(f'selected: {e.selection}'),
    )
    ui.radio({None: 'none', 'single': 'single', 'multiple': 'multiple'},
             on_change=lambda e: table.set_selection(e.value))


@doc.demo('Table with expandable rows', '''
    Scoped slots can be used to insert buttons that toggle the expand state of a table row.
    See the [Quasar documentation](https://quasar.dev/vue-components/table#expanding-rows) for more information.
''')
def table_with_expandable_rows():
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]
    rows = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol'},
    ]

    table = ui.table(columns=columns, rows=rows, row_key='name').classes('w-72')
    table.add_slot('header', r'''
        <q-tr :props="props">
            <q-th auto-width />
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
            </q-th>
        </q-tr>
    ''')
    table.add_slot('body', r'''
        <q-tr :props="props">
            <q-td auto-width>
                <q-btn size="sm" color="accent" round dense
                    @click="props.expand = !props.expand"
                    :icon="props.expand ? 'remove' : 'add'" />
            </q-td>
            <q-td v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.value }}
            </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
            <q-td colspan="100%">
                <div class="text-left">This is {{ props.row.name }}.</div>
            </q-td>
        </q-tr>
    ''')


@doc.demo('Show and hide columns', '''
    Here is an example of how to show and hide columns in a table.
''')
def show_and_hide_columns():
    from typing import Dict

    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
        {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
    ]
    rows = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol'},
    ]
    table = ui.table(columns=columns, rows=rows, row_key='name')

    def toggle(column: Dict, visible: bool) -> None:
        column['classes'] = '' if visible else 'hidden'
        column['headerClasses'] = '' if visible else 'hidden'
        table.update()

    with ui.button(icon='menu'):
        with ui.menu(), ui.column().classes('gap-0 p-2'):
            for column in columns:
                ui.switch(column['label'], value=True, on_change=lambda e,
                          column=column: toggle(column, e.value))


@doc.demo('Table with drop down selection', '''
    Here is an example of how to use a drop down selection in a table.
    After emitting a `rename` event from the scoped slot, the `rename` function updates the table rows.
''')
def table_with_drop_down_selection():
    from nicegui import events

    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]
    rows = [
        {'id': 0, 'name': 'Alice', 'age': 18},
        {'id': 1, 'name': 'Bob', 'age': 21},
        {'id': 2, 'name': 'Carol'},
    ]
    name_options = ['Alice', 'Bob', 'Carol']

    def rename(e: events.GenericEventArguments) -> None:
        for row in rows:
            if row['id'] == e.args['id']:
                row['name'] = e.args['name']
        ui.notify(f'Table.rows is now: {table.rows}')

    table = ui.table(columns=columns, rows=rows).classes('w-full')
    table.add_slot('body-cell-name', r'''
        <q-td key="name" :props="props">
            <q-select
                v-model="props.row.name"
                :options="''' + str(name_options) + r'''"
                @update:model-value="() => $parent.$emit('rename', props.row)"
            />
        </q-td>
    ''')
    table.on('rename', rename)


@doc.demo('Table from Pandas DataFrame', '''
    You can create a table from a Pandas DataFrame using the `from_pandas` method.
    This method takes a Pandas DataFrame as input and returns a table.
''')
def table_from_pandas_demo():
    import pandas as pd

    df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    ui.table.from_pandas(df).classes('max-h-40')


@doc.demo('Table from Polars DataFrame', '''
    You can create a table from a Polars DataFrame using the `from_polars` method.
    This method takes a Polars DataFrame as input and returns a table.

    *Added in version 2.7.0*
''')
def table_from_polars_demo():
    import polars as pl

    df = pl.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    ui.table.from_polars(df).classes('max-h-40')


@doc.demo('Adding rows', '''
    It's simple to add new rows with the `add_row(dict)` and `add_rows(list[dict])` methods.
    With the "virtual-scroll" prop set, the table can be programmatically scrolled with the `scrollTo` JavaScript function.
''')
def adding_rows():
    from datetime import datetime

    def add():
        table.add_row({'date': datetime.now().strftime('%c')})
        table.run_method('scrollTo', len(table.rows)-1)

    columns = [{'name': 'date', 'label': 'Date', 'field': 'date'}]
    table = ui.table(columns=columns, rows=[]).classes('h-52').props('virtual-scroll')
    ui.button('Add row', on_click=add)


@doc.demo('Custom sorting and formatting', '''
    You can define dynamic column attributes using a `:` prefix.
    This way you can define custom sorting and formatting functions.

    The following example allows sorting the `name` column by length.
    The `age` column is formatted to show the age in years.
''')
def custom_formatting():
    columns = [
        {
            'name': 'name',
            'label': 'Name',
            'field': 'name',
            'sortable': True,
            ':sort': '(a, b, rowA, rowB) => b.length - a.length',
        },
        {
            'name': 'age',
            'label': 'Age',
            'field': 'age',
            ':format': 'value => value + " years"',
        },
    ]
    rows = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carl', 'age': 42},
    ]
    ui.table(columns=columns, rows=rows, row_key='name')


@doc.demo('Toggle fullscreen', '''
    You can toggle the fullscreen mode of a table using the `toggle_fullscreen()` method.
''')
def toggle_fullscreen():
    table = ui.table(
        columns=[{'name': 'name', 'label': 'Name', 'field': 'name'}],
        rows=[{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Carol'}],
    ).classes('w-full')

    with table.add_slot('top-left'):
        def toggle() -> None:
            table.toggle_fullscreen()
            button.props('icon=fullscreen_exit' if table.is_fullscreen else 'icon=fullscreen')
        button = ui.button('Toggle fullscreen', icon='fullscreen', on_click=toggle).props('flat')


@doc.demo('Pagination', '''
    You can provide either a single integer or a dictionary to define pagination.

    The dictionary can contain the following keys:

    - `rowsPerPage`: The number of rows per page.
    - `sortBy`: The column name to sort by.
    - `descending`: Whether to sort in descending order.
    - `page`: The current page (1-based).
''')
def pagination() -> None:
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
        {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
    ]
    rows = [
        {'name': 'Elsa', 'age': 18},
        {'name': 'Oaken', 'age': 46},
        {'name': 'Hans', 'age': 20},
        {'name': 'Sven'},
        {'name': 'Olaf', 'age': 4},
        {'name': 'Anna', 'age': 17},
    ]
    ui.table(columns=columns, rows=rows, pagination=3)
    ui.table(columns=columns, rows=rows, pagination={'rowsPerPage': 4, 'sortBy': 'age', 'page': 2})


@doc.demo('Handle pagination changes', '''
    You can handle pagination changes using the `on_pagination_change` parameter.
''')
def handle_pagination_changes() -> None:
    ui.table(
        columns=[{'id': 'Name', 'label': 'Name', 'field': 'Name', 'align': 'left'}],
        rows=[{'Name': f'Person {i}'} for i in range(100)],
        pagination=3,
        on_pagination_change=lambda e: ui.notify(e.value),
    )


@doc.demo('Computed props', '''
    You can access the computed props of a table within async callback functions.
''')
def computed_props():
    async def show_filtered_sorted_rows():
        ui.notify(await table.get_filtered_sorted_rows())

    async def show_computed_rows():
        ui.notify(await table.get_computed_rows())

    table = ui.table(
        columns=[
            {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left', 'sortable': True},
            {'name': 'age', 'label': 'Age', 'field': 'age', 'align': 'left', 'sortable': True}
        ],
        rows=[
            {'name': 'Noah', 'age': 33},
            {'name': 'Emma', 'age': 21},
            {'name': 'Rose', 'age': 88},
            {'name': 'James', 'age': 59},
            {'name': 'Olivia', 'age': 62},
            {'name': 'Liam', 'age': 18},
        ],
        row_key='name',
        pagination=3,
    )
    ui.input('Search by name/age').bind_value(table, 'filter')
    ui.button('Show filtered/sorted rows', on_click=show_filtered_sorted_rows)
    ui.button('Show computed rows', on_click=show_computed_rows)


@doc.demo('Computed fields', '''
    You can use functions to compute the value of a column.
    The function receives the row as an argument.
    See the [Quasar documentation](https://quasar.dev/vue-components/table#defining-the-columns) for more information.
''')
def computed_fields():
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left'},
        {'name': 'length', 'label': 'Length', ':field': 'row => row.name.length'},
    ]
    rows = [
        {'name': 'Alice'},
        {'name': 'Bob'},
        {'name': 'Christopher'},
    ]
    ui.table(columns=columns, rows=rows, row_key='name')


@doc.demo('Conditional formatting', '''
    You can use scoped slots to conditionally format the content of a cell.
    See the [Quasar documentation](https://quasar.dev/vue-components/table#example--body-cell-slot)
    for more information about body-cell slots.

    In this demo we use a `q-badge` to display the age in red if the person is under 21 years old.
    We use the `body-cell-age` slot to insert the `q-badge` into the `age` column.
    The ":color" attribute of the `q-badge` is set to "red" if the age is under 21, otherwise it is set to "green".
    The colon in front of the "color" attribute indicates that the value is a JavaScript expression.
''')
def conditional_formatting():
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]
    rows = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol', 'age': 42},
    ]
    table = ui.table(columns=columns, rows=rows, row_key='name')
    table.add_slot('body-cell-age', '''
        <q-td key="age" :props="props">
            <q-badge :color="props.value < 21 ? 'red' : 'green'">
                {{ props.value }}
            </q-badge>
        </q-td>
    ''')


@doc.demo('Table cells with links', '''
    Here is a demo of how to insert links into table cells.
    We use the `body-cell-link` slot to insert an `<a>` tag into the `link` column.
''')
def table_cells_with_links():
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left'},
        {'name': 'link', 'label': 'Link', 'field': 'link', 'align': 'left'},
    ]
    rows = [
        {'name': 'Google', 'link': 'https://google.com'},
        {'name': 'Facebook', 'link': 'https://facebook.com'},
        {'name': 'Twitter', 'link': 'https://twitter.com'},
    ]
    table = ui.table(columns=columns, rows=rows, row_key='name')
    table.add_slot('body-cell-link', '''
        <q-td :props="props">
            <a :href="props.value">{{ props.value }}</a>
        </q-td>
    ''')


@doc.demo('Table with masonry-like grid', '''
    You can use the `grid` prop to display the table as a masonry-like grid.
    See the [Quasar documentation](https://quasar.dev/vue-components/table#grid-style) for more information.
''')
def table_with_masonry_like_grid():
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]
    rows = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol', 'age': 42},
    ]
    table = ui.table(columns=columns, rows=rows, row_key='name').props('grid')
    table.add_slot('item', r'''
        <q-card flat bordered :props="props" class="m-1">
            <q-card-section class="text-center">
                <strong>{{ props.row.name }}</strong>
            </q-card-section>
            <q-separator />
            <q-card-section class="text-center">
                <div>{{ props.row.age }} years</div>
            </q-card-section>
        </q-card>
    ''')


doc.reference(ui.table)
