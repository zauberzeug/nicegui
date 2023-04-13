from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from nicegui import ui

from .screen import Screen


def test_update_table(screen: Screen):
    grid = ui.aggrid({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [{'name': 'Alice', 'age': 18}],
    })

    screen.open('/')
    screen.should_contain('Name')
    screen.should_contain('Age')
    screen.should_contain('Alice')
    screen.should_contain('18')

    grid.options['rowData'][0]['age'] = 42
    grid.update()
    screen.should_contain('42')


def test_add_row(screen: Screen):
    grid = ui.aggrid({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [],
    })
    ui.button('Update', on_click=grid.update)

    screen.open('/')
    grid.options['rowData'].append({'name': 'Alice', 'age': 18})
    screen.click('Update')
    screen.wait(0.5)
    screen.should_contain('Alice')
    screen.should_contain('18')
    grid.options['rowData'].append({'name': 'Bob', 'age': 21})
    screen.click('Update')
    screen.wait(0.5)
    screen.should_contain('Alice')
    screen.should_contain('18')
    screen.should_contain('Bob')
    screen.should_contain('21')


def test_click_cell(screen: Screen):
    grid = ui.aggrid({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [{'name': 'Alice', 'age': 18}],
    })
    grid.on('cellClicked', lambda msg: ui.label(f'{msg["args"]["data"]["name"]} has been clicked!'))

    screen.open('/')
    screen.click('Alice')
    screen.should_contain('Alice has been clicked!')


def test_html_columns(screen: Screen):
    ui.aggrid({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [{'name': '<span class="text-bold">Alice</span>', 'age': 18}],
    }, html_columns=[0])

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_not_contain('<span')
    assert 'text-bold' in screen.find('Alice').get_attribute('class')


def test_call_api_method_with_argument(screen: Screen):
    grid = ui.aggrid({
        'columnDefs': [{'field': 'name', 'filter': True}],
        'rowData': [{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Carol'}],
    })
    filter = {'name': {'filterType': 'text', 'type': 'equals', 'filter': 'Alice'}}
    ui.button('Filter', on_click=lambda: grid.call_api_method('setFilterModel', filter))

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Carol')
    screen.click('Filter')
    screen.should_contain('Alice')
    screen.should_not_contain('Bob')
    screen.should_not_contain('Carol')


def test_get_selected_rows(screen: Screen):
    grid = ui.aggrid({
        'columnDefs': [{'field': 'name'}],
        'rowData': [{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Carol'}],
        'rowSelection': 'multiple',
    })

    async def get_selected_rows():
        ui.label(str(await grid.get_selected_rows()))
    ui.button('Get selected rows', on_click=get_selected_rows)

    async def get_selected_row():
        ui.label(str(await grid.get_selected_row()))
    ui.button('Get selected row', on_click=get_selected_row)

    screen.open('/')
    screen.click('Alice')
    screen.find('Bob')
    ActionChains(screen.selenium).key_down(Keys.SHIFT).click(screen.find('Bob')).key_up(Keys.SHIFT).perform()
    screen.click('Get selected rows')
    screen.should_contain("[{'name': 'Alice'}, {'name': 'Bob'}]")

    screen.click('Get selected row')
    screen.should_contain("{'name': 'Alice'}")


def test_create_from_pandas(screen: Screen):
    import pandas as pd
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [18, 21]})
    ui.aggrid.from_pandas(df)

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('18')
    screen.should_contain('21')
