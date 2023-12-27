from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


def test_change_chart_series(screen: Screen):
    chart = ui.highchart({
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['A', 'B']},
        'series': [
            {'name': 'Alpha', 'data': [0.1, 0.2]},
            {'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    }).classes('w-full h-64')

    def update():
        chart.options['series'][0]['data'][:] = [1, 1]
        chart.update()

    ui.button('Update', on_click=update)

    def get_series_0():
        return screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-series-0 .highcharts-point')

    screen.open('/')
    screen.wait(0.5)
    before = [bar.size['width'] for bar in get_series_0()]  # pylint: disable=disallowed-name
    screen.click('Update')
    screen.wait(0.5)
    after = [bar.size['width'] for bar in get_series_0()]  # pylint: disable=disallowed-name
    assert before[0] < after[0]
    assert before[1] < after[1]


def test_adding_chart_series(screen: Screen):
    chart = ui.highchart({
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['A', 'B']},
        'series': [],
    }).classes('w-full h-64')

    def add():
        chart.options['series'].append({'name': 'X', 'data': [0.1, 0.2]})
        chart.update()
    ui.button('Add', on_click=add)

    screen.open('/')
    screen.click('Add')
    screen.wait(0.5)
    assert len(screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-point')) == 3


def test_removing_chart_series(screen: Screen):
    chart = ui.highchart({
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['A', 'B']},
        'series': [
            {'name': 'Alpha', 'data': [0.1, 0.2]},
            {'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    }).classes('w-full h-64')

    def remove():
        chart.options['series'].pop(0)
        chart.update()
    ui.button('Remove', on_click=remove)

    screen.open('/')
    screen.click('Remove')
    screen.wait(0.5)
    assert len(screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-point')) == 3


def test_missing_extra(screen: Screen):
    # NOTE: This test does not work after test_extra() has been run, because conftest won't reset libraries correctly.
    ui.highchart({'chart': {'type': 'solidgauge'}})

    screen.open('/')
    assert not screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-pane')


def test_extra(screen: Screen):
    ui.highchart({'chart': {'type': 'solidgauge'}}, extras=['solid-gauge'])

    screen.open('/')
    assert screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-pane')


def test_stock_chart(screen: Screen):
    ui.highchart({}, type='stockChart', extras=['stock'])

    screen.open('/')
    assert screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-range-selector-buttons')


def test_replace_chart(screen: Screen):
    with ui.row() as container:
        ui.highchart({'series': [{'name': 'A'}]})

    def replace():
        container.clear()
        with container:
            ui.highchart({'series': [{'name': 'B'}]})
    ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')
    screen.click('Replace')
    screen.should_contain('B')
    screen.should_not_contain('A')


def test_updating_stock_chart(screen: Screen):
    """https://github.com/zauberzeug/nicegui/discussions/948"""
    chart = ui.highchart({'legend': {'enabled': True}, 'series': []}, type='stockChart', extras=['stock'])
    ui.button('update', on_click=lambda: (
        chart.options['series'].extend([{'name': 'alice'}, {'name': 'bob'}]),
        chart.update(),
    ))
    ui.button('clear', on_click=lambda: (
        chart.options['series'].clear(),
        chart.update(),
    ))

    screen.open('/')
    screen.click('update')
    screen.should_contain('alice')
    screen.should_contain('bob')
    screen.click('clear')
    screen.wait(0.5)
    screen.should_not_contain('alice')
    screen.should_not_contain('bob')


def test_create_dynamically(screen: Screen):
    ui.button('Create', on_click=lambda: ui.highchart({}))

    screen.open('/')
    screen.click('Create')
    screen.should_contain('Chart title')
