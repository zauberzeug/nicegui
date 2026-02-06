from datetime import datetime, timedelta, timezone

import pandas as pd
import polars as pl
import pytest
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import SharedScreen


def columns() -> list:
    return [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True},
        {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
    ]


def rows() -> list:
    return [
        {'id': 0, 'name': 'Alice', 'age': 18},
        {'id': 1, 'name': 'Bob', 'age': 21},
        {'id': 2, 'name': 'Lionel', 'age': 19},
    ]


def test_table(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.table(title='My Team', columns=columns(), rows=rows())

    shared_screen.open('/')
    shared_screen.should_contain('My Team')
    shared_screen.should_contain('Name')
    shared_screen.should_contain('Alice')
    shared_screen.should_contain('Bob')
    shared_screen.should_contain('Lionel')


def test_pagination_int(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.table(columns=columns(), rows=rows(), pagination=2)

    shared_screen.open('/')
    shared_screen.should_contain('Alice')
    shared_screen.should_contain('Bob')
    shared_screen.should_not_contain('Lionel')
    shared_screen.should_contain('1-2 of 3')


def test_pagination_dict(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.table(columns=columns(), rows=rows(), pagination={'rowsPerPage': 2})

    shared_screen.open('/')
    shared_screen.should_contain('Alice')
    shared_screen.should_contain('Bob')
    shared_screen.should_not_contain('Lionel')
    shared_screen.should_contain('1-2 of 3')


def test_filter(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        table = ui.table(columns=columns(), rows=rows())
        ui.input('Search by name').bind_value(table, 'filter')

    shared_screen.open('/')
    shared_screen.should_contain('Alice')
    shared_screen.should_contain('Bob')
    shared_screen.should_contain('Lionel')

    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Search by name"]')
    element.send_keys('e')
    shared_screen.should_contain('Alice')
    shared_screen.should_not_contain('Bob')
    shared_screen.should_contain('Lionel')


def test_add_remove(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        table = ui.table(columns=columns(), rows=rows())
        ui.button('Add', on_click=lambda: table.add_row({'id': 3, 'name': 'Carol', 'age': 32}))
        ui.button('Remove', on_click=lambda: table.remove_row(table.rows[0]))

    shared_screen.open('/')
    shared_screen.click('Add')
    shared_screen.should_contain('Carol')

    shared_screen.click('Remove')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Alice')


def test_slots(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.table(columns=columns(), rows=rows()) as table:
            table.add_slot('top-row', '''
                <q-tr>
                    <q-th>This is the top slot.</q-th>
                </q-tr>
            ''')
            table.add_slot('body', '''
                <q-tr :props="props">
                    <q-td key="name" :props="props">overridden</q-td>
                    <q-td key="age" :props="props">
                        <q-badge color="green">{{ props.row.age }}</q-badge>
                    </q-td>
                </q-tr>
            ''')

    shared_screen.open('/')
    shared_screen.should_contain('This is the top slot.')
    shared_screen.should_not_contain('Alice')
    shared_screen.should_contain('overridden')
    shared_screen.should_contain('21')


def test_selection(shared_screen: SharedScreen):
    table = None

    @ui.page('/')
    def page():
        nonlocal table
        table = ui.table(columns=columns(), rows=rows(), selection='single')
        ui.radio({None: 'none', 'single': 'single', 'multiple': 'multiple'},
                 on_change=lambda e: table.set_selection(e.value))

    shared_screen.open('/')
    shared_screen.find('Alice').find_element(By.XPATH, 'preceding-sibling::td').click()
    shared_screen.wait(0.5)
    shared_screen.should_contain('1 record selected.')

    shared_screen.find('Bob').find_element(By.XPATH, 'preceding-sibling::td').click()
    shared_screen.wait(0.5)
    shared_screen.should_contain('1 record selected.')

    shared_screen.click('multiple')
    shared_screen.wait(0.5)

    shared_screen.find('Lionel').find_element(By.XPATH, 'preceding-sibling::td').click()
    shared_screen.wait(0.5)
    shared_screen.should_contain('2 records selected.')
    assert table.selection == 'multiple'

    shared_screen.click('none')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('1 record selected.')
    assert table.selection is None


def test_dynamic_column_attributes(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.table(columns=[{'name': 'age', 'label': 'Age', 'field': 'age', ':format': 'value => value + " years"'}],
                 rows=[{'name': 'Alice', 'age': 18}])

    shared_screen.open('/')
    shared_screen.should_contain('18 years')


def test_remove_selection(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        t = ui.table(columns=columns(), rows=rows(), selection='single')
        ui.button('Remove first row', on_click=lambda: t.remove_row(t.rows[0]))

    shared_screen.open('/')
    shared_screen.find('Alice').find_element(By.XPATH, 'preceding-sibling::td').click()
    shared_screen.should_contain('1 record selected.')

    shared_screen.click('Remove first row')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Alice')
    shared_screen.should_not_contain('1 record selected.')


def test_replace_rows(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        t = ui.table(columns=columns(), rows=rows())

        def replace_rows_with_carol():
            t.rows = [{'id': 3, 'name': 'Carol', 'age': 32}]

        def replace_rows_with_daniel():
            t.update_rows([{'id': 4, 'name': 'Daniel', 'age': 33}])

        ui.button('Replace rows with C.', on_click=replace_rows_with_carol)
        ui.button('Replace rows with D.', on_click=replace_rows_with_daniel)

    shared_screen.open('/')
    shared_screen.should_contain('Alice')
    shared_screen.should_contain('Bob')
    shared_screen.should_contain('Lionel')

    shared_screen.click('Replace rows with C.')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Alice')
    shared_screen.should_not_contain('Bob')
    shared_screen.should_not_contain('Lionel')
    shared_screen.should_contain('Carol')

    shared_screen.click('Replace rows with D.')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Carol')
    shared_screen.should_contain('Daniel')


@pytest.mark.parametrize('df_type', ['pandas', 'polars'])
def test_create_and_update_from_df(shared_screen: SharedScreen, df_type: str):
    @ui.page('/')
    def page():
        if df_type == 'pandas':
            DataFrame = pd.DataFrame
            df = DataFrame({'name': ['Alice', 'Bob'], 'age': [18, 21]})
            table = ui.table.from_pandas(df)
            update_from_df = table.update_from_pandas
        else:
            DataFrame = pl.DataFrame
            df = DataFrame({'name': ['Alice', 'Bob'], 'age': [18, 21]})
            table = ui.table.from_polars(df)
            update_from_df = table.update_from_polars

        ui.button('Update', on_click=lambda: update_from_df(DataFrame({'name': ['Lionel'], 'age': [19]})))

    shared_screen.open('/')
    shared_screen.should_contain('Alice')
    shared_screen.should_contain('Bob')
    shared_screen.should_contain('18')
    shared_screen.should_contain('21')

    shared_screen.click('Update')
    shared_screen.should_contain('Lionel')
    shared_screen.should_contain('19')


@pytest.mark.parametrize('df_type', ['pandas', 'polars'])
def test_problematic_datatypes(shared_screen: SharedScreen, df_type: str):
    @ui.page('/')
    def page():
        if df_type == 'pandas':
            df = pd.DataFrame({
                'Datetime_col': [datetime(2020, 1, 1)],
                'Datetime_col_tz': [datetime(2020, 1, 2, tzinfo=timezone.utc)],
                'Timedelta_col': [timedelta(days=5)],
                'Complex_col': [1 + 2j],
                'Period_col': pd.Series([pd.Period('2021-01')]),
            })
            ui.table.from_pandas(df)
        else:
            df = pl.DataFrame({
                'Datetime_col': [datetime(2020, 1, 1)],
                'Datetime_col_tz': [datetime(2020, 1, 2, tzinfo=timezone.utc)],
            })
            ui.table.from_polars(df)

    shared_screen.open('/')
    shared_screen.should_contain('Datetime_col')
    shared_screen.should_contain('2020-01-01')
    shared_screen.should_contain('Datetime_col_tz')
    shared_screen.should_contain('2020-01-02')
    if df_type == 'pandas':
        shared_screen.should_contain('Timedelta_col')
        shared_screen.should_contain('5 days')
        shared_screen.should_contain('Complex_col')
        shared_screen.should_contain('(1+2j)')
        shared_screen.should_contain('Period_col')
        shared_screen.should_contain('2021-01')


def test_table_computed_props(shared_screen: SharedScreen):
    all_rows = rows()
    filtered_rows = [row for row in all_rows if 'e' in row['name']]
    filtered_sorted_rows = sorted(filtered_rows, key=lambda row: row['age'], reverse=True)

    @ui.page('/')
    async def page():
        table = ui.table(
            columns=columns(),
            rows=all_rows,
            row_key='id',
            selection='multiple',
            pagination={'rowsPerPage': 1, 'sortBy': 'age', 'descending': True})
        table.filter = 'e'

        await ui.context.client.connected()
        assert filtered_sorted_rows == await table.get_filtered_sorted_rows()
        assert filtered_sorted_rows[:1] == await table.get_computed_rows()
        assert len(filtered_sorted_rows) == await table.get_computed_rows_number()

    shared_screen.open('/')
    shared_screen.should_contain('Lionel')
    shared_screen.should_not_contain('Alice')
    shared_screen.should_not_contain('Bob')


def test_infer_columns(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.table(rows=[
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
        ])

    shared_screen.open('/')
    shared_screen.should_contain('NAME')
    shared_screen.should_contain('AGE')
    shared_screen.should_contain('Alice')
    shared_screen.should_contain('Bob')
    shared_screen.should_contain('18')
    shared_screen.should_contain('21')


def test_default_column_parameters(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.table(rows=[
            {'name': 'Alice', 'age': 18, 'city': 'London'},
            {'name': 'Bob', 'age': 21, 'city': 'Paris'},
        ], columns=[
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'age', 'label': 'Age', 'field': 'age'},
            {'name': 'city', 'label': 'City', 'field': 'city', 'sortable': False},
        ], column_defaults={'sortable': True})

    shared_screen.open('/')
    shared_screen.should_contain('Name')
    shared_screen.should_contain('Age')
    shared_screen.should_contain('Alice')
    shared_screen.should_contain('Bob')
    shared_screen.should_contain('18')
    shared_screen.should_contain('21')
    shared_screen.should_contain('London')
    shared_screen.should_contain('Paris')
    assert len(shared_screen.find_all_by_class('sortable')) == 2


@pytest.mark.parametrize('df_type', ['pandas', 'polars'])
def test_columns_from_df(shared_screen: SharedScreen, df_type: str):
    @ui.page('/')
    def page():
        if df_type == 'pandas':
            persons = ui.table.from_pandas(pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [18, 21]}))
            cars = ui.table.from_pandas(pd.DataFrame({'make': ['Ford', 'Toyota'], 'model': ['Focus', 'Corolla']}),
                                        columns=[{'name': 'make', 'label': 'make', 'field': 'make'}])
            DataFrame = pd.DataFrame
            update_persons_from_df = persons.update_from_pandas
            update_cars_from_df = cars.update_from_pandas
        else:
            persons = ui.table.from_polars(pl.DataFrame({'name': ['Alice', 'Bob'], 'age': [18, 21]}))
            cars = ui.table.from_polars(pl.DataFrame({'make': ['Ford', 'Toyota'], 'model': ['Focus', 'Corolla']}),
                                        columns=[{'name': 'make', 'label': 'make', 'field': 'make'}])
            DataFrame = pl.DataFrame
            update_persons_from_df = persons.update_from_polars
            update_cars_from_df = cars.update_from_polars

        ui.button('Update persons without columns',
                  on_click=lambda: update_persons_from_df(DataFrame({'name': ['Dan'], 'age': [5], 'sex': ['male']})))

        ui.button('Update persons with columns',
                  on_click=lambda: update_persons_from_df(DataFrame({'name': ['Stephen'], 'age': [33]}),
                                                          columns=[{'name': 'name', 'label': 'Name', 'field': 'name'}]))

        ui.button('Update cars without columns',
                  on_click=lambda: update_cars_from_df(DataFrame({'make': ['Honda'], 'model': ['Civic']})))

        ui.button('Update cars with columns',
                  on_click=lambda: update_cars_from_df(DataFrame({'make': ['Hyundai'], 'model': ['i30']}),
                                                       columns=[{'name': 'make', 'label': 'make', 'field': 'make'},
                                                                {'name': 'model', 'label': 'model', 'field': 'model'}]))

    shared_screen.open('/')
    shared_screen.should_contain('name')
    shared_screen.should_contain('age')
    shared_screen.should_contain('make')
    shared_screen.should_not_contain('model')

    shared_screen.click('Update persons without columns')  # infer columns (like during instantiation)
    shared_screen.should_contain('Dan')
    shared_screen.should_contain('5')
    shared_screen.should_contain('male')

    shared_screen.click('Update persons with columns')  # updated columns via parameter
    shared_screen.should_contain('Stephen')
    shared_screen.should_not_contain('32')

    shared_screen.click('Update cars without columns')  # don't change columns
    shared_screen.should_contain('Honda')
    shared_screen.should_not_contain('Civic')

    shared_screen.click('Update cars with columns')  # updated columns via parameter
    shared_screen.should_contain('Hyundai')
    shared_screen.should_contain('i30')


def test_new_slots(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        table = ui.table(rows=[{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Carol'}])
        with table.add_slot('body-cell-name'):
            with table.cell():
                ui.button().props(':label="props.value"') \
                    .on('click', js_handler='() => emit(props.value)', handler=lambda e: ui.notify(f'Clicked {e.args}'))

    shared_screen.open('/')
    shared_screen.should_contain('Alice')

    shared_screen.click('Alice')
    shared_screen.should_contain('Clicked Alice')
