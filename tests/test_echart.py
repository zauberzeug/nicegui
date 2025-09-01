from collections.abc import Generator

import pytest
from pyecharts import options
from pyecharts.charts import Bar
from pyecharts.commons import utils

from nicegui import app, ui
from nicegui.testing import Screen


@pytest.fixture
def test_route() -> Generator[str, None, None]:
    TEST_ROUTE = '/theme.json'
    yield TEST_ROUTE
    app.remove_route(TEST_ROUTE)


def test_create_dynamically(screen: Screen):
    @ui.page('/')
    def page():
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
    @ui.page('/')
    def page():
        def update():
            chart.options['xAxis'] = {'type': 'value'}
            chart.options['yAxis'] = {'type': 'category', 'data': ['A', 'B', 'C']}
            chart.options['series'] = [{'type': 'line', 'data': [0.1, 0.2, 0.3]}]
        chart = ui.echart({})
        ui.button('Update', on_click=update)

    screen.open('/')
    assert not screen.find_all_by_tag('canvas')

    screen.click('Update')
    assert screen.find_by_tag('canvas')


def test_nested_card(screen: Screen):
    @ui.page('/')
    def page():
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
    @ui.page('/')
    def page():
        with ui.expansion() as expansion:
            with ui.card().style('height: 200px; width: 600px'):
                ui.echart({
                    'xAxis': {'type': 'value'},
                    'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
                    'series': [{'type': 'line', 'data': [0.1, 0.2, 0.3]}],
                    'animationDuration': 100,
                })
        ui.button('Open', on_click=expansion.open)

    screen.open('/')
    screen.click('Open')
    screen.wait(0.5)
    canvas = screen.find_by_tag('canvas')
    assert canvas.rect['height'] == 168
    assert canvas.rect['width'] == 568


def test_run_method(screen: Screen):
    @ui.page('/')
    def page():
        echart = ui.echart({
            'xAxis': {'type': 'value'},
            'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
            'series': [{'type': 'line', 'data': [0.1, 0.2, 0.3]}],
        }).style('width: 600px')

        async def get_width():
            ui.label(f'Width: {await echart.run_chart_method("getWidth")}px')
        ui.button('Get Width', on_click=get_width)

    screen.open('/')
    screen.click('Get Width')
    screen.should_contain('Width: 600px')


def test_create_from_pyecharts(screen: Screen):
    X_AXIS_FORMATTER = r'(val, idx) => `x for ${val}`'
    Y_AXIS_FORMATTER = r'(val, idx) => `${val} kg`'

    @ui.page('/')
    def page():
        ui.echart.from_pyecharts(
            Bar()
            .add_xaxis(['A', 'B', 'C'])
            .add_yaxis('series A', [0.1, 0.2, 0.3],)
            .set_global_opts(
                xaxis_opts=options.AxisOpts(axislabel_opts={':formatter': X_AXIS_FORMATTER}),
                yaxis_opts=options.AxisOpts(axislabel_opts={'formatter': utils.JsCode(Y_AXIS_FORMATTER)}),
            )
        ).props('renderer=svg')

    screen.open('/')
    screen.should_contain('x for A')
    screen.should_contain('x for B')
    screen.should_contain('x for C')
    screen.should_contain('0.1 kg')
    screen.should_contain('0.2 kg')
    screen.should_contain('0.3 kg')


def test_chart_events(screen: Screen):
    @ui.page('/')
    def page():
        ui.echart({
            'xAxis': {'type': 'category'},
            'yAxis': {'type': 'value'},
            'series': [{'type': 'line', 'data': [1, 2, 3]}],
        }).on('chart:rendered', lambda: ui.label('Chart rendered.'))

    screen.open('/')
    screen.should_contain('Chart rendered.')


def test_theme_dictionary(screen: Screen):
    @ui.page('/')
    def page():
        ui.echart({
            'xAxis': {'type': 'category'},
            'yAxis': {'type': 'value'},
            'series': [{'type': 'line', 'data': [1, 2, 3]}],
        }, theme={'backgroundColor': 'rgba(254,248,239,1)'}, renderer='svg')

    screen.open('/')
    assert screen.find_by_tag('rect').value_of_css_property('fill') == 'rgb(254, 248, 239)'


def test_theme_url(screen: Screen, test_route: str):  # pylint: disable=redefined-outer-name
    @app.get(test_route)
    def theme():
        return {'backgroundColor': 'rgba(254,248,239,1)'}

    @ui.page('/')
    def page():
        ui.echart({
            'xAxis': {'type': 'category'},
            'yAxis': {'type': 'value'},
            'series': [{'type': 'line', 'data': [1, 2, 3]}],
        }, theme=test_route, renderer='svg')

    screen.open('/')
    assert screen.find_by_tag('rect').value_of_css_property('fill') == 'rgb(254, 248, 239)'
