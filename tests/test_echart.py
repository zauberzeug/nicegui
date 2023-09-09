from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


def test_create_dynamically(screen: Screen):
    def create():
        ui.echart({
            'xAxis': {'type': 'value'},
            'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
            'series': [
                {'type': 'line', 'data': [0.1, 0.2, 0.3],},
            ],
        })
    ui.button('Create', on_click=lambda: create())

    screen.open('/')
    screen.click('Create')
    assert screen.find_by_tag('canvas')

def test_update(screen: Screen):
    def update_chart():
        chart.options['xAxis'] = {'type': 'value'}
        chart.options['yAxis'] = {'type': 'category', 'data': ['A', 'B', 'C']}
        chart.options['series'] = [
                {'type': 'line', 'data': [0.1, 0.2, 0.3],},
            ]
        chart.update()
    chart = ui.echart({})
    ui.button('Update', on_click=lambda: update_chart())
    screen.open('/')
    try:
        screen.find_by_tag('canvas')
        raise AssertionError(f'Canvas should not be rendered')
    except:
        screen.click('Update')
        assert screen.find_by_tag('canvas')

def test_nested_card(screen: Screen):
    def create():
        ui.echart({
            'xAxis': {'type': 'value'},
            'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
            'series': [
                {'type': 'line', 'data': [0.1, 0.2, 0.3],},
            ],
        })
    with ui.card().style('height: 200px').style('width: 600px'):
        create()

    screen.open('/')
    canvas = screen.find_by_tag('canvas')
    assert canvas.rect['height'] == 168
    assert canvas.rect['width'] == 568
