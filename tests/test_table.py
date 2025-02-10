import sys
from datetime import datetime, timedelta, timezone
from typing import List

import pandas as pd
import polars as pl
import pytest
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


def columns() -> List:
    return [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True},
        {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
    ]


def rows() -> List:
    return [
        {'id': 0, 'name': 'Alice', 'age': 18},
        {'id': 1, 'name': 'Bob', 'age': 21},
        {'id': 2, 'name': 'Lionel', 'age': 19},
    ]


def test_table(screen: Screen):
    ui.table(title='My Team', columns=columns(), rows=rows())

    screen.open('/')
    screen.should_contain('My Team')
    screen.should_contain('Name')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Lionel')


def test_pagination_int(screen: Screen):
    ui.table(columns=columns(), rows=rows(), pagination=2)

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_not_contain('Lionel')
    screen.should_contain('1-2 of 3')


def test_pagination_dict(screen: Screen):
    ui.table(columns=columns(), rows=rows(), pagination={'rowsPerPage': 2})

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_not_contain('Lionel')
    screen.should_contain('1-2 of 3')


def test_filter(screen: Screen):
    table = ui.table(columns=columns(), rows=rows())
    ui.input('Search by name').bind_value(table, 'filter')

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Lionel')

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Search by name"]')
    element.send_keys('e')
    screen.should_contain('Alice')
    screen.should_not_contain('Bob')
    screen.should_contain('Lionel')


def test_add_remove(screen: Screen):
    table = ui.table(columns=columns(), rows=rows())
    ui.button('Add', on_click=lambda: table.add_row({'id': 3, 'name': 'Carol', 'age': 32}))
    ui.button('Remove', on_click=lambda: table.remove_row(table.rows[0]))

    screen.open('/')
    screen.click('Add')
    screen.should_contain('Carol')

    screen.click('Remove')
    screen.wait(0.5)
    screen.should_not_contain('Alice')


def test_slots(screen: Screen):
    with ui.table(columns=columns(), rows=rows()) as table:
        with table.add_slot('top-row'):
            with table.row():
                with table.cell():
                    ui.label('This is the top slot.')
        table.add_slot('body', '''
            <q-tr :props="props">
                <q-td key="name" :props="props">overridden</q-td>
                <q-td key="age" :props="props">
                    <q-badge color="green">{{ props.row.age }}</q-badge>
                </q-td>
            </q-tr>
        ''')

    screen.open('/')
    screen.should_contain('This is the top slot.')
    screen.should_not_contain('Alice')
    screen.should_contain('overridden')
    screen.should_contain('21')


def test_selection(screen: Screen):
    table = ui.table(columns=columns(), rows=rows(), selection='single')
    ui.radio({None: 'none', 'single': 'single', 'multiple': 'multiple'},
             on_change=lambda e: table.set_selection(e.value))

    screen.open('/')
    screen.find('Alice').find_element(By.XPATH, 'preceding-sibling::td').click()
    screen.wait(0.5)
    screen.should_contain('1 record selected.')

    screen.find('Bob').find_element(By.XPATH, 'preceding-sibling::td').click()
    screen.wait(0.5)
    screen.should_contain('1 record selected.')

    screen.click('multiple')
    screen.wait(0.5)

    screen.find('Lionel').find_element(By.XPATH, 'preceding-sibling::td').click()
    screen.wait(0.5)
    screen.should_contain('2 records selected.')
    assert table.selection == 'multiple'

    screen.click('none')
    screen.wait(0.5)
    screen.should_not_contain('1 record selected.')
    assert table.selection is None


def test_dynamic_column_attributes(screen: Screen):
    ui.table(columns=[{'name': 'age', 'label': 'Age', 'field': 'age', ':format': 'value => value + " years"'}],
             rows=[{'name': 'Alice', 'age': 18}])

    screen.open('/')
    screen.should_contain('18 years')


def test_remove_selection(screen: Screen):
    t = ui.table(columns=columns(), rows=rows(), selection='single')
    ui.button('Remove first row', on_click=lambda: t.remove_row(t.rows[0]))

    screen.open('/')
    screen.find('Alice').find_element(By.XPATH, 'preceding-sibling::td').click()
    screen.should_contain('1 record selected.')

    screen.click('Remove first row')
    screen.wait(0.5)
    screen.should_not_contain('Alice')
    screen.should_not_contain('1 record selected.')


def test_replace_rows(screen: Screen):
    t = ui.table(columns=columns(), rows=rows())

    def replace_rows_with_carol():
        t.rows = [{'id': 3, 'name': 'Carol', 'age': 32}]

    def replace_rows_with_daniel():
        t.update_rows([{'id': 4, 'name': 'Daniel', 'age': 33}])

    ui.button('Replace rows with C.', on_click=replace_rows_with_carol)
    ui.button('Replace rows with D.', on_click=replace_rows_with_daniel)

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Lionel')

    screen.click('Replace rows with C.')
    screen.wait(0.5)
    screen.should_not_contain('Alice')
    screen.should_not_contain('Bob')
    screen.should_not_contain('Lionel')
    screen.should_contain('Carol')

    screen.click('Replace rows with D.')
    screen.wait(0.5)
    screen.should_not_contain('Carol')
    screen.should_contain('Daniel')


@pytest.mark.parametrize('df_type', ['pandas', 'polars'])
def test_create_and_update_from_df(screen: Screen, df_type: str):
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

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('18')
    screen.should_contain('21')

    screen.click('Update')
    screen.should_contain('Lionel')
    screen.should_contain('19')


@pytest.mark.parametrize('df_type', ['pandas', 'polars'])
@pytest.mark.skipif(sys.version_info[:2] == (3, 8), reason='Skipping test for Python 3.8')
def test_problematic_datatypes(screen: Screen, df_type: str):
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

    screen.open('/')
    screen.should_contain('Datetime_col')
    screen.should_contain('2020-01-01')
    screen.should_contain('Datetime_col_tz')
    screen.should_contain('2020-01-02')
    if df_type == 'pandas':
        screen.should_contain('Timedelta_col')
        screen.should_contain('5 days')
        screen.should_contain('Complex_col')
        screen.should_contain('(1+2j)')
        screen.should_contain('Period_col')
        screen.should_contain('2021-01')


def test_table_computed_props(screen: Screen):
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

    screen.open('/')
    screen.should_contain('Lionel')
    screen.should_not_contain('Alice')
    screen.should_not_contain('Bob')


def test_infer_columns(screen: Screen):
    ui.table(rows=[
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
    ])

    screen.open('/')
    screen.should_contain('NAME')
    screen.should_contain('AGE')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('18')
    screen.should_contain('21')


def test_default_column_parameters(screen: Screen):
    ui.table(rows=[
        {'name': 'Alice', 'age': 18, 'city': 'London'},
        {'name': 'Bob', 'age': 21, 'city': 'Paris'},
    ], columns=[
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
        {'name': 'city', 'label': 'City', 'field': 'city', 'sortable': False},
    ], column_defaults={'sortable': True})

    screen.open('/')
    screen.should_contain('Name')
    screen.should_contain('Age')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('18')
    screen.should_contain('21')
    screen.should_contain('London')
    screen.should_contain('Paris')
    assert len(screen.find_all_by_class('sortable')) == 2


@pytest.mark.parametrize('df_type', ['pandas', 'polars'])
def test_columns_from_df(screen: Screen, df_type: str):
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

    screen.open('/')
    screen.should_contain('name')
    screen.should_contain('age')
    screen.should_contain('make')
    screen.should_not_contain('model')

    screen.click('Update persons without columns')  # infer columns (like during instantiation)
    screen.should_contain('Dan')
    screen.should_contain('5')
    screen.should_contain('male')

    screen.click('Update persons with columns')  # updated columns via parameter
    screen.should_contain('Stephen')
    screen.should_not_contain('32')

    screen.click('Update cars without columns')  # don't change columns
    screen.should_contain('Honda')
    screen.should_not_contain('Civic')

    screen.click('Update cars with columns')  # updated columns via parameter
    screen.should_contain('Hyundai')
    screen.should_contain('i30')
