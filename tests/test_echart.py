from nicegui import ui

from .screen import Screen


def test_create_dynamically(screen: Screen):
    def create():
        ui.echart({
            'xAxis': {'type': 'value'},
            'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
            'series': [{'type': 'line', 'data': [0.1, 0.2, 0.3]}],
        })
    ui.button('Create', on_click=create)

    screen.open('/')
    screen.click('Create')
    assert screen.find_by_tag('canvas')


def test_update(screen: Screen):
    def update():
        chart.options['xAxis'] = {'type': 'value'}
        chart.options['yAxis'] = {'type': 'category', 'data': ['A', 'B', 'C']}
        chart.options['series'] = [{'type': 'line', 'data': [0.1, 0.2, 0.3]}]
        chart.update()
    chart = ui.echart({})
    ui.button('Update', on_click=update)

    screen.open('/')
    assert not screen.find_all_by_tag('canvas')
    screen.click('Update')
    assert screen.find_by_tag('canvas')


def test_nested_card(screen: Screen):
    with ui.card().style('height: 200px; width: 600px'):
        ui.echart({
            'xAxis': {'type': 'value'},
            'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
            'series': [{'type': 'line', 'data': [0.1, 0.2, 0.3]}],
        })

    screen.open('/')
    canvas = screen.find_by_tag('canvas')
    assert canvas.rect['height'] == 168
    assert canvas.rect['width'] == 568


def test_nested_expansion(screen: Screen):
    with ui.expansion() as expansion:
        with ui.card().style('height: 200px; width: 600px'):
            ui.echart({
                'xAxis': {'type': 'value'},
                'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
                'series': [{'type': 'line', 'data': [0.1, 0.2, 0.3]}],
            })
    ui.button('Open', on_click=expansion.open)

    screen.open('/')
    screen.click('Open')
    canvas = screen.find_by_tag('canvas')
    assert canvas.rect['height'] == 168
    assert canvas.rect['width'] == 568


def test_run_method(screen: Screen):
    echart = ui.echart({
        'xAxis': {'type': 'value'},
        'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
        'series': [{'type': 'line', 'data': [0.1, 0.2, 0.3]}],
    }).classes('w-[600px]')

    async def get_width():
        ui.label(f'Width: {await echart.run_chart_method("getWidth")}px')
    ui.button('Get Width', on_click=get_width)

    screen.open('/')
    screen.click('Get Width')
    screen.should_contain('Width: 600px')
