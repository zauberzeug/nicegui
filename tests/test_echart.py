from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


def test_change_chart_series(screen: Screen):
    chart = ui.echart({
        'xAxis': {'type': 'value'},
        'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},
        'legend': {'textStyle': {'color': 'gray'}},
        'series': [
            {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},
            {'type': 'bar', 'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    }).classes('w-full h-64')

    def update():
        chart.options['series'][0]['data'][:] = [1, 1]
        chart.update()

    ui.button('Update', on_click=update)

    # to be updated to for ehcart testing
    #
    # def get_series_0():
    #     return screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-series-0 .highcharts-point')
    # 
    # screen.open('/')
    # screen.wait(0.5)
    # before = [bar.size['width'] for bar in get_series_0()]  # pylint: disable=disallowed-name
    # screen.click('Update')
    # screen.wait(0.5)
    # after = [bar.size['width'] for bar in get_series_0()]  # pylint: disable=disallowed-name
    # assert before[0] < after[0]
    # assert before[1] < after[1]


def test_adding_chart_series(screen: Screen):
    chart = ui.echart({
        'xAxis': {'type': 'category', 'data': ['A', 'B']},
        'series': [],
    }).classes('w-full h-64')

    def add():
        chart.options['series'].append({'type':'bar', 'name': 'X', 'data': [0.1, 0.2]})
        chart.update()
    ui.button('Add', on_click=add)

    # to be updated to for ehcart testing
    # 
    # screen.open('/')
    # screen.click('Add')
    # screen.wait(0.5)
    # assert len(screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-point')) == 3


def test_removing_chart_series(screen: Screen):
    chart = ui.echart({
        'xAxis': {'type': 'category', 'data': ['A', 'B']},
        'series': [
            {'type':'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},
            {'type':'bar', 'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    }).classes('w-full h-64')

    def remove():
        chart.options['series'].pop(0)
        chart.update()
    ui.button('Remove', on_click=remove)

    # to be updated to for ehcart testing
    #
    # screen.open('/')
    # screen.click('Remove')
    # screen.wait(0.5)
    # assert len(screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-point')) == 3

def test_replace_chart(screen: Screen):
    with ui.row() as container:
        ui.echart({'series': [{'type':'bar', 'name': 'A'}]})

    def replace():
        container.clear()
        with container:
            ui.echart({'series': [{'type':'bar', 'name': 'B'}]})
    ui.button('Replace', on_click=replace)

    # to be updated to for ehcart testing
    #
    # screen.open('/')
    # screen.should_contain('A')
    # screen.click('Replace')
    # screen.should_contain('B')
    # screen.should_not_contain('A')

def test_create_dynamically(screen: Screen):
    ui.button('Create', on_click=lambda: ui.echart({}))

    # to be updated to for ehcart testing
    #
    # screen.open('/')
    # screen.click('Create')
    # screen.should_contain('Chart title')
