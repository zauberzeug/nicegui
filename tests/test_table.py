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


def test_table_with_lists_in_rows(screen: Screen):
    """Test that tables handle lists in row data without causing memory issues."""
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'tags', 'label': 'Tags', 'field': 'tags'},
        {'name': 'scores', 'label': 'Scores', 'field': 'scores'},
    ]

    rows = [
        {'name': 'Alice', 'tags': ['python', 'django'], 'scores': [95, 87, 92]},
        {'name': 'Bob', 'tags': ['javascript', 'react'], 'scores': [88, 91, 85]},
        {'name': 'Carol', 'tags': 'single-tag', 'scores': 90},  # Mixed types
    ]

    table = ui.table(columns=columns, rows=rows, row_key='name')

    screen.open('/')

    # Verify content is displayed (lists converted to strings)
    screen.should_contain('Alice')
    screen.should_contain("['python', 'django']")
    screen.should_contain('[95, 87, 92]')
    screen.should_contain('Bob')
    screen.should_contain("['javascript', 'react']")
    screen.should_contain('Carol')
    screen.should_contain('single-tag')  # Non-list should remain unchanged

    # Verify that the internal data is sanitized
    assert isinstance(table.rows[0]['tags'], str)
    assert isinstance(table.rows[0]['scores'], str)
    assert table.rows[2]['tags'] == 'single-tag'  # Non-list unchanged


def test_table_add_rows_with_lists(screen: Screen):
    """Test adding rows with lists to existing table."""
    table = ui.table(columns=columns(), rows=rows())

    def add_row_with_list():
        table.add_row({'id': 3, 'name': 'Carol', 'age': [25, 26, 27]})  # Age as list

    ui.button('Add row with list', on_click=add_row_with_list)

    screen.open('/')
    screen.click('Add row with list')
    screen.should_contain('Carol')
    screen.should_contain('[25, 26, 27]')

    # Verify internal data is sanitized
    assert isinstance(table.rows[-1]['age'], str)


def test_table_list_sanitization_comprehensive(screen: Screen):
    """Comprehensive test for list sanitization in tables."""

    # Test 1: Constructor sanitization
    rows_with_lists = [
        {'id': 1, 'data': ['a', 'b', 'c']},
        {'id': 2, 'data': (1, 2, 3)},
    ]
    table = ui.table(
        columns=[{'name': 'id', 'field': 'id'}, {'name': 'data', 'field': 'data'}],
        rows=rows_with_lists,
        row_key='id'
    )

    screen.open('/')

    assert isinstance(table.rows[0]['data'], str)
    assert isinstance(table.rows[1]['data'], str)

    # Test 2: Property setter sanitization
    table.rows = [{'id': 3, 'data': {'set', 'data'}}]
    assert isinstance(table.rows[0]['data'], str)

    # Test 3: add_row sanitization
    table.add_row({'id': 4, 'data': [1, 2, [3, 4]]})
    assert isinstance(table.rows[-1]['data'], str)

    # Test 4: add_rows sanitization
    table.add_rows([
        {'id': 5, 'data': ('tuple', 'data')},
        {'id': 6, 'data': ['more', 'list', 'data']}
    ])
    assert all(isinstance(row['data'], str) for row in table.rows[-2:])

    # Test 5: update_rows sanitization
    table.update_rows([
        {'id': 7, 'data': {'set1', 'set2'}},
        {'id': 8, 'data': [True, False, None]}
    ])
    assert all(isinstance(row['data'], str) for row in table.rows)


def test_sanitize_rows_unit():
    """Unit test for the _sanitize_rows method."""
    from nicegui.elements.table import Table

    # Test data with various types
    test_rows = [
        {'id': 1, 'list_data': [1, 2, 3]},
        {'id': 2, 'tuple_data': (4, 5, 6)},
        {'id': 3, 'set_data': {7, 8, 9}},
        {'id': 4, 'dict_data': {'key': 'value'}},  # Should be converted to string
        {'id': 5, 'string_data': 'hello'},  # Should remain unchanged
        {'id': 6, 'int_data': 42},  # Should remain unchanged
        {'id': 7, 'none_data': None},  # Should remain unchanged
        {'id': 8, 'nested_list': [1, [2, 3], 4]},  # Nested structures
    ]

    sanitized = Table._sanitize_rows(test_rows)

    # Lists, tuples, sets, and dicts should be converted to strings
    assert isinstance(sanitized[0]['list_data'], str)
    assert sanitized[0]['list_data'] == '[1, 2, 3]'

    assert isinstance(sanitized[1]['tuple_data'], str)
    assert sanitized[1]['tuple_data'] == '(4, 5, 6)'

    assert isinstance(sanitized[2]['set_data'], str)
    set_str = sanitized[2]['set_data']
    assert '7' in set_str and '8' in set_str and '9' in set_str

    # Dictionaries should also be converted to strings
    assert isinstance(sanitized[3]['dict_data'], str)
    assert sanitized[3]['dict_data'] == "{'key': 'value'}"

    # Other types should remain unchanged
    assert isinstance(sanitized[4]['string_data'], str)
    assert sanitized[4]['string_data'] == 'hello'
    assert isinstance(sanitized[5]['int_data'], int)
    assert sanitized[5]['int_data'] == 42
    assert sanitized[6]['none_data'] is None
    assert isinstance(sanitized[7]['nested_list'], str)


def test_table_nested_complex_data(screen: Screen):
    """Test handling of deeply nested complex structures."""
    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'data', 'label': 'Data', 'field': 'data'},
    ]

    rows = [
        {'id': 1, 'data': {'nested': ['list', 'inside', 'dict']}},  # Nested structures
        {'id': 2, 'data': [{'dict': 'inside'}, {'list': 'here'}]},  # Complex nesting
    ]

    table = ui.table(columns=columns, rows=rows, row_key='id')

    screen.open('/')  # Establish proper context

    # All complex structures should be stringified
    assert all(isinstance(row['data'], str) for row in table.rows)


def test_table_performance_with_lists(screen: Screen):
    """Test that large tables with lists perform acceptably."""
    import time

    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'tags', 'label': 'Tags', 'field': 'tags'},
    ]

    # Create many rows with lists
    rows = []
    for i in range(1000):
        rows.append({
            'id': i,
            'tags': [f'tag_{j}' for j in range(10)],  # Each row has a list of 10 items
        })

    start_time = time.time()
    table = ui.table(columns=columns, rows=rows, row_key='id')
    creation_time = time.time() - start_time

    screen.open('/')  # Establish proper context

    # Should complete quickly (within reasonable time)
    assert creation_time < 5.0, f'Table creation took too long: {creation_time:.2f}s'

    # Verify data is sanitized
    assert all(isinstance(row['tags'], str) for row in table.rows)

    # Test adding more data
    start_time = time.time()
    table.add_rows([{'id': i + 1000, 'tags': [f'new_tag_{j}' for j in range(5)]}
                   for i in range(100)])
    add_time = time.time() - start_time

    assert add_time < 2.0, f'Adding rows took too long: {add_time:.2f}s'


def test_table_lists_no_browser_crash(screen: Screen):
    """Test the exact scenario from GitHub issue #4837."""
    columns = [
        {'name': 'col1', 'label': 'Column 1', 'field': 'col1', 'required': True},
        {'name': 'col2', 'label': 'Column 2', 'field': 'col2'},
        {'name': 'col3', 'label': 'Column 3', 'field': 'col3', 'required': True},
    ]

    # This is the exact data from the GitHub issue that caused crashes
    rows = [
        {'col1': '1 Data point', 'col2': '1 Data point', 'col3': '1 Data point'},
        {'col1': '2 Data point', 'col2': '2 Data point', 'col3': '2 Data point'},
        {'col1': '3 Data point', 'col2': '3 Data point', 'col3': '3 Data point'},
        {'col1': '4 Data point', 'col2': '4 Data point', 'col3': ['Point 1', 'Point 2', 'Point 3']},
    ]

    table = ui.table(columns=columns, rows=rows, row_key='col1')

    screen.open('/')

    # Should render without crashing
    screen.should_contain('1 Data point')
    screen.should_contain('4 Data point')
    screen.should_contain("['Point 1', 'Point 2', 'Point 3']")

    # Verify sanitization occurred
    assert isinstance(table.rows[3]['col3'], str)
    assert table.rows[3]['col3'] == "['Point 1', 'Point 2', 'Point 3']"
