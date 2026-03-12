import inspect
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import polars as pl
import pytest
from fastapi.responses import FileResponse
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from nicegui import Event, app, ui
from nicegui.testing import Screen


def test_update_table(screen: Screen):
    @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [{'field': 'name'}, {'field': 'age'}],
            'rowData': [{'name': 'Alice', 'age': 18}],
        })
        ui.button('Change age', on_click=lambda: grid.options['rowData'][0].update(age=42))

    screen.open('/')
    screen.should_contain('Name')
    screen.should_contain('Age')
    screen.should_contain('Alice')
    screen.should_contain('18')

    screen.click('Change age')
    screen.should_contain('42')


def test_add_row(screen: Screen):
    @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [{'field': 'name'}, {'field': 'age'}],
            'rowData': [],
        })
        ui.button('Update', on_click=grid.update)
        ui.button('Add Alice', on_click=lambda: grid.options['rowData'].append({'name': 'Alice', 'age': 18}))
        ui.button('Add Bob', on_click=lambda: grid.options['rowData'].append({'name': 'Bob', 'age': 21}))

    screen.open('/')
    screen.click('Add Alice')
    screen.click('Update')
    screen.should_contain('Alice')
    screen.should_contain('18')

    screen.click('Add Bob')
    screen.click('Update')
    screen.should_contain('Bob')
    screen.should_contain('21')


def test_click_cell(screen: Screen):
    @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [{'field': 'name'}, {'field': 'age'}],
            'rowData': [{'name': 'Alice', 'age': 18}],
        })
        grid.on('cellClicked', lambda e: ui.label(f'{e.args["data"]["name"]} has been clicked!'))

    screen.open('/')
    screen.click('Alice')
    screen.should_contain('Alice has been clicked!')


def test_html_columns(screen: Screen):
    @ui.page('/')
    def page():
        ui.aggrid({
            'columnDefs': [{'field': 'name'}, {'field': 'age'}],
            'rowData': [{'name': '<span class="text-bold">Alice</span>', 'age': 18}],
        }, html_columns=[0])

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_not_contain('<span')
    assert 'text-bold' in screen.find('Alice').get_attribute('class')


def test_dynamic_method(screen: Screen):
    @ui.page('/')
    def page():
        ui.aggrid({
            'columnDefs': [{'field': 'name'}, {'field': 'age'}],
            'rowData': [{'name': 'Alice', 'age': '18'}, {'name': 'Bob', 'age': '21'}, {'name': 'Carol', 'age': '42'}],
            ':getRowHeight': 'params => params.data.age > 35 ? 50 : 25',
        })

    screen.open('/')
    trs = screen.find_all_by_class('ag-row')
    assert len(trs) == 3
    heights = [int(tr.get_attribute('clientHeight')) for tr in trs]
    assert 23 <= heights[0] <= 25
    assert 23 <= heights[1] <= 25
    assert 48 <= heights[2] <= 50


def test_run_grid_method_with_argument(screen: Screen):
    @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [{'field': 'name', 'filter': True}],
            'rowData': [{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Carol'}],
        })
        filter_model = {'name': {'filterType': 'text', 'type': 'equals', 'filter': 'Alice'}}
        ui.button('Filter', on_click=lambda: grid.run_grid_method('setFilterModel', filter_model))

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Carol')

    screen.click('Filter')
    screen.wait(0.5)
    screen.should_contain('Alice')
    screen.should_not_contain('Bob')
    screen.should_not_contain('Carol')


def test_get_selected_rows(screen: Screen):
    @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [{'field': 'name'}],
            'rowData': [{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Carol'}],
            'rowSelection': {'mode': 'multiRow', 'enableClickSelection': True},
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


def test_replace_aggrid(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row().classes('w-full') as container:
            ui.aggrid({'columnDefs': [{'field': 'name'}], 'rowData': [{'name': 'Alice'}]})

        def replace():
            with container.clear():
                ui.aggrid({'columnDefs': [{'field': 'name'}], 'rowData': [{'name': 'Bob'}]})
        ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('Alice')

    screen.click('Replace')
    screen.should_contain('Bob')
    screen.should_not_contain('Alice')


@pytest.mark.parametrize('df_type', ['pandas', 'polars'])
def test_create_from_dataframe(screen: Screen, df_type: str):
    @ui.page('/')
    def page():
        if df_type == 'pandas':
            df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [18, 21], 42: 'answer'})
            ui.aggrid.from_pandas(df)
        else:
            df = pl.DataFrame({'name': ['Alice', 'Bob'], 'age': [18, 21], '42': 'answer'})
            ui.aggrid.from_polars(df)

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('18')
    screen.should_contain('21')
    screen.should_contain('42')
    screen.should_contain('answer')


def test_create_dynamically(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('Create',
                  on_click=lambda: ui.aggrid({'columnDefs': [{'field': 'name'}], 'rowData': [{'name': 'Alice'}]}))

    screen.open('/')
    screen.click('Create')
    screen.should_contain('Alice')


def test_api_method_after_creation(screen: Screen):
    @ui.page('/')
    def page():
        options = {'columnDefs': [{'field': 'name'}], 'rowData': [{'name': 'Ed'}], 'rowSelection': {'mode': 'multiRow'}}
        ui.button('Create', on_click=lambda: ui.aggrid(options).run_grid_method('selectAll'))

    screen.open('/')
    screen.click('Create')
    assert screen.find_by_class('ag-row-selected')


def test_set_module_source(screen: Screen):
    get_aggrid: Event[[]] = Event()

    @app.get('/custom-aggrid.js')
    def custom_aggrid():
        get_aggrid.emit()
        return FileResponse(Path(inspect.getfile(ui.aggrid)).parent / 'dist' / 'index.js')

    ui.aggrid.set_module_source('/custom-aggrid.js')

    @ui.page('/')
    async def page():
        get_aggrid.subscribe(lambda: ui.notify('Load custom bundle'))

        aggrid = ui.aggrid({}, modules=['ClientSideRowModelModule', 'ColumnAutoSizeModule', 'EventApiModule'])

        await ui.context.client.connected()
        for module in ['ClipboardModule', 'ColumnAutoSizeModule', 'EventApiModule']:
            is_registered = await ui.run_javascript(f'getElement({aggrid.id}).api.isModuleRegistered("{module}")')
            ui.label(f'{module}: {is_registered}')

    screen.open('/')
    screen.should_contain('Load custom bundle')
    screen.should_contain('ClipboardModule: False')
    screen.should_contain('ColumnAutoSizeModule: True')
    screen.should_contain('EventApiModule: True')


@pytest.mark.parametrize('df_type', ['pandas', 'polars'])
def test_problematic_datatypes(screen: Screen, df_type: str):
    @ui.page('/')
    def page():
        if df_type == 'pandas':
            df = pd.DataFrame({
                'datetime_col': [datetime(2020, 1, 1)],
                'datetime_col_tz': [datetime(2020, 1, 2, tzinfo=timezone.utc)],
                'timedelta_col': [timedelta(days=5)],
                'complex_col': [1 + 2j],
                'period_col': pd.Series([pd.Period('2021-01')]),
            })
            ui.aggrid.from_pandas(df)
        else:
            df = pl.DataFrame({
                'datetime_col': [datetime(2020, 1, 1)],
                'datetime_col_tz': [datetime(2020, 1, 2, tzinfo=timezone.utc)],
            })
            ui.aggrid.from_polars(df)

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


def test_run_row_method(screen: Screen):
    @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [{'field': 'name'}, {'field': 'age'}],
            'rowData': [{'name': 'Alice', 'age': 18}],
            ':getRowId': '(params) => params.data.name',
        })
        ui.button('Update', on_click=lambda: grid.run_row_method('Alice', 'setDataValue', 'age', 42))

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('18')

    screen.click('Update')
    screen.should_contain('Alice')
    screen.should_contain('42')


def test_run_grid_method_xss(screen: Screen):
    @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [{'field': 'name'}],
            'rowData': [{'name': 'Alice'}, {'name': 'Bob'}],
        })
        ui.button('XSS 1', on_click=lambda: grid.run_grid_method('console.error("X" + "SS")'))
        ui.button('XSS 2', on_click=lambda: grid.run_grid_method('x", console.error("X" + "SS"), "y'))

    screen.allowed_js_errors.append('Method "console.error("X" + "SS")" not found.')
    screen.allowed_js_errors.append('Method "x", console.error("X" + "SS"), "y" not found.')
    screen.open('/')
    screen.click('XSS 1')
    screen.click('XSS 2')
    screen.wait(1)
    assert 'XSS' not in screen.render_js_logs()
    screen.assert_py_logger('ERROR', 'Method "console.error("X" + "SS")" not found.')
    screen.assert_py_logger('ERROR', 'Method "x", console.error("X" + "SS"), "y" not found.')


def test_get_client_data(screen: Screen):
    data: list = []

    @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [
                {'field': 'name'},
                {'field': 'age', 'sort': 'desc'},
            ],
            'rowData': [
                {'name': 'Alice', 'age': 18},
                {'name': 'Bob', 'age': 21},
                {'name': 'Carol', 'age': 42},
            ],
        })

        async def get_data():
            data[:] = await grid.get_client_data()
        ui.button('Get Data', on_click=get_data)

        async def get_sorted_data():
            data[:] = await grid.get_client_data(method='filtered_sorted')
        ui.button('Get Sorted Data', on_click=get_sorted_data)

    screen.open('/')
    screen.click('Get Data')
    screen.wait(0.5)
    assert data == [{'name': 'Alice', 'age': 18}, {'name': 'Bob', 'age': 21}, {'name': 'Carol', 'age': 42}]

    screen.click('Get Sorted Data')
    screen.wait(0.5)
    assert data == [{'name': 'Carol', 'age': 42}, {'name': 'Bob', 'age': 21}, {'name': 'Alice', 'age': 18}]


def test_version_matches_js(screen: Screen):
    @ui.page('/')
    async def page():
        ui.label(await ui.run_javascript('return (await import("nicegui-aggrid")).AllCommunityModule.version'))

    screen.open('/')
    screen.should_contain(ui.aggrid.VERSION)
