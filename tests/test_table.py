from datetime import datetime, timedelta, timezone
from typing import List

import pandas as pd
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


def columns() -> List:
    return [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]


def rows() -> List:
    return [
        {'id': 0, 'name': 'Alice', 'age': 18},
        {'id': 1, 'name': 'Bob', 'age': 21},
        {'id': 2, 'name': 'Lionel', 'age': 19},
    ]


def df() -> pd.DataFrame:
    return pd.DataFrame({'name': ['Patrick', 'Liz'], 'age': [24, 40], 42: 'answer'})


def test_table(screen: Screen):
    ui.table(title='My Team', columns=columns(), rows=rows())

    screen.open('/')
    screen.should_contain('My Team')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Lionel')

    screen.should_not_contain('id')  # when providing columns, only those columns are shown
    screen.should_contain('Name')  # the label should be displayed as provided


def test_table_without_columns(screen: Screen):
    ui.table(title='My Team', rows=rows())

    screen.open('/')
    screen.should_contain('My Team')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Lionel')

    screen.should_contain('ID')  # when omitting columns, they are inferred from the first row and capitalized


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
    ui.button('Add', on_click=lambda: table.add_rows({'id': 3, 'name': 'Carol', 'age': 32}))
    ui.button('Remove', on_click=lambda: table.remove_rows(table.rows[0]))

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


def test_single_selection(screen: Screen):
    ui.table(columns=columns(), rows=rows(), selection='single')

    screen.open('/')
    screen.find('Alice').find_element(By.XPATH, 'preceding-sibling::td').click()
    screen.wait(0.5)
    screen.should_contain('1 record selected.')

    screen.find('Bob').find_element(By.XPATH, 'preceding-sibling::td').click()
    screen.wait(0.5)
    screen.should_contain('1 record selected.')


def test_dynamic_column_attributes(screen: Screen):
    ui.table(columns=[{'name': 'age', 'label': 'Age', 'field': 'age', ':format': 'value => value + " years"'}],
             rows=[{'name': 'Alice', 'age': 18}])

    screen.open('/')
    screen.should_contain('18 years')


def test_remove_selection(screen: Screen):
    t = ui.table(columns=columns(), rows=rows(), selection='single')
    ui.button('Remove first row', on_click=lambda: t.remove_rows(t.rows[0]))

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


def test_update_columns(screen: Screen):
    t = ui.table(columns=columns(), rows=rows())

    def replace_columns():
        t.columns = [{'name': 'name', 'label': 'Nombre', 'field': 'name', 'sortable': True}]

    ui.button('Replace columns', on_click=replace_columns)

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Lionel')
    assert len(screen.find_all_by_class('sortable')) == 0

    screen.click('Replace columns')
    screen.should_contain('Nombre')
    screen.should_not_contain('Name')
    screen.should_not_contain('Age')
    assert len(screen.find_all_by_class('sortable')) == 1


def test_create_from_dataframe(screen: Screen):
    ui.table(df=df())

    screen.open('/')
    screen.should_contain('NAME')
    screen.should_contain('Patrick')
    screen.should_contain('Liz')
    screen.should_contain('AGE')
    screen.should_contain('24')
    screen.should_contain('40')
    screen.should_contain('42')
    screen.should_contain('answer')


def test_create_from_dataframe_with_problematic_datatypes(screen: Screen):
    df = pd.DataFrame({
        'Datetime_col': [datetime(2020, 1, 1)],
        'Datetime_col_tz': [datetime(2020, 1, 1, tzinfo=timezone.utc)],
        'Timedelta_col': [timedelta(days=5)],
        'Complex_col': [1 + 2j],
        'Period_col': pd.Series([pd.Period('2021-01')]),
    })
    ui.table(df=df)

    screen.open('/')
    screen.should_contain('DATETIME_COL')
    screen.should_contain('DATETIME_COL_TZ')
    screen.should_contain('TIMEDELTA_COL')
    screen.should_contain('COMPLEX_COL')
    screen.should_contain('PERIOD_COL')
    screen.should_contain('2020-01-01')
    screen.should_contain('5 days')
    screen.should_contain('(1+2j)')
    screen.should_contain('2021-01')


def test_create_from_dataframe_with_custom_columns(screen: Screen):
    ui.table(df=df(), columns=[
        {'name': 'first_name', 'label': 'First name', 'field': 'name', 'headerClasses': 'my-class'},
        {'name': 'age', 'label': 'Double the age', 'field': 'age', 'sortable': True, ':format': '(val, _row) => 2*val'}
    ])

    screen.open('/')
    screen.should_contain('First name')
    screen.should_contain('48')
    assert len(screen.find_all_by_css('th.my-class')) == 1
    assert len(screen.find_all_by_class('sortable')) == 1


def test_update_dataframe(screen: Screen):
    table = ui.table(df=df())

    def update_df() -> None:
        table.df = pd.DataFrame({'name': ['Alice', 'Lionel'], 'age': [18, 22], 42: 'answer'})

    ui.button('Replace df', on_click=update_df)

    screen.open('/')
    screen.should_contain('Patrick')
    screen.should_contain('Liz')
    screen.should_contain('24')
    screen.should_contain('40')

    screen.click('Replace df')
    screen.should_contain('Alice')
    screen.should_contain('Lionel')
    screen.should_not_contain('Patrick')
    screen.should_contain('18')
    screen.should_contain('22')
    screen.should_not_contain('24')


def test_both_rows_and_dataframe(screen: Screen):
    table = ui.table(df=df(), rows=rows(), columns=columns())

    def update_df() -> None:
        table.df = pd.DataFrame({'name': ['Mike', 'Pamela'], 'age': [70, 26], 42: 'answer'})
    ui.button('Update df', on_click=update_df)

    def update_rows():
        table.rows = [{'id': 3, 'name': 'Carol', 'age': 32}]
    ui.button('Update rows', on_click=update_rows)

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Lionel')
    screen.should_contain('Patrick')
    screen.should_contain('Liz')
    screen.should_contain('24')
    screen.should_contain('40')
    screen.should_contain('18')
    screen.should_contain('19')
    screen.should_contain('21')

    screen.click('Update df')
    screen.should_contain('Mike')
    screen.should_contain('Alice')
    screen.should_not_contain('Patrick')

    screen.click('Update rows')
    screen.should_contain('Carol')
    screen.should_contain('Mike')
    screen.should_not_contain('Alice')


def test_default_column(screen: Screen):
    ui.table(columns=columns(), rows=rows(), default_column={'sortable': True})

    screen.open('/')
    screen.should_contain('Alice')
    assert len(screen.find_all_by_class('sortable')) == 2


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
