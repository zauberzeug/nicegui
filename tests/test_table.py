from datetime import datetime, timedelta
from typing import List

import pandas as pd
from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


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


def test_create_from_pandas(screen: Screen):
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [18, 21], 42: 'answer'})
    ui.table.from_pandas(df)

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('18')
    screen.should_contain('21')
    screen.should_contain('42')
    screen.should_contain('answer')


def test_problematic_datatypes(screen: Screen):
    df = pd.DataFrame({
        'Datetime_col': [datetime(2020, 1, 1)],
        'Timedelta_col': [timedelta(days=5)],
        'Complex_col': [1 + 2j],
        'Period_col': pd.Series([pd.Period('2021-01')]),
    })
    ui.table.from_pandas(df)

    screen.open('/')
    screen.should_contain('Datetime_col')
    screen.should_contain('Timedelta_col')
    screen.should_contain('Complex_col')
    screen.should_contain('Period_col')
    screen.should_contain('2020-01-01')
    screen.should_contain('5 days')
    screen.should_contain('(1+2j)')
    screen.should_contain('2021-01')
