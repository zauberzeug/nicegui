from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


def get_series_0(selenium):
    return selenium.find_elements(By.CSS_SELECTOR, '.highcharts-series-0 .highcharts-point')


def test_change_chart_data(screen: Screen):
    chart = ui.chart({
        'title': False,
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

    screen.open('/')
    screen.wait(.5)
    before = [bar.size['width'] for bar in get_series_0(screen.selenium)]
    screen.click('Update')
    screen.wait(.5)
    after = [bar.size['width'] for bar in get_series_0(screen.selenium)]
    assert before[0] < after[0]
    assert before[1] < after[1]
