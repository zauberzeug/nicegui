from collections.abc import Generator

import pytest
from pyecharts import options
from pyecharts.charts import Bar
from pyecharts.commons import utils

from nicegui import app, ui
from nicegui.testing import SharedScreen


@pytest.fixture
def test_route() -> Generator[str, None, None]:
    TEST_ROUTE = '/theme.json'
    yield TEST_ROUTE
    app.remove_route(TEST_ROUTE)


def test_create_dynamically(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        def create():
            ui.echart({
                'xAxis': {'type': 'value'},
                'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
                'series': [{'type': 'line', 'data': [0.1, 0.2, 0.3]}],
            })
        ui.button('Create', on_click=create)

    shared_screen.open('/')
    shared_screen.click('Create')
    assert shared_screen.find_by_tag('canvas')


def test_update(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        def update():
            chart.options['xAxis'] = {'type': 'value'}
            chart.options['yAxis'] = {'type': 'category', 'data': ['A', 'B', 'C']}
            chart.options['series'] = [{'type': 'line', 'data': [0.1, 0.2, 0.3]}]
        chart = ui.echart({})
        ui.button('Update', on_click=update)

    shared_screen.open('/')
    assert not shared_screen.find_all_by_tag('canvas')

    shared_screen.click('Update')
    assert shared_screen.find_by_tag('canvas')


def test_nested_card(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.card().style('height: 200px; width: 600px'):
            ui.echart({
                'xAxis': {'type': 'value'},
                'yAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
                'series': [{'type': 'line', 'data': [0.1, 0.2, 0.3]}],
            })

    shared_screen.open('/')
    canvas = shared_screen.find_by_tag('canvas')
    assert canvas.rect['height'] == 168
    assert canvas.rect['width'] == 568


def test_nested_expansion(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('Open')
    shared_screen.wait(0.5)
    canvas = shared_screen.find_by_tag('canvas')
    assert canvas.rect['height'] == 168
    assert canvas.rect['width'] == 568


def test_run_method(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('Get Width')
    shared_screen.should_contain('Width: 600px')


def test_create_from_pyecharts(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.should_contain('x for A')
    shared_screen.should_contain('x for B')
    shared_screen.should_contain('x for C')
    shared_screen.should_contain('0.1 kg')
    shared_screen.should_contain('0.2 kg')
    shared_screen.should_contain('0.3 kg')


def test_chart_events(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.echart({
            'xAxis': {'type': 'category'},
            'yAxis': {'type': 'value'},
            'series': [{'type': 'line', 'data': [1, 2, 3]}],
        }).on('chart:rendered', lambda: ui.label('Chart rendered.'))

    shared_screen.open('/')
    shared_screen.should_contain('Chart rendered.')


def test_theme_dictionary(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.echart({
            'xAxis': {'type': 'category'},
            'yAxis': {'type': 'value'},
            'series': [{'type': 'line', 'data': [1, 2, 3]}],
        }, theme={'backgroundColor': 'rgba(254,248,239,1)'}, renderer='svg')

    shared_screen.open('/')
    assert shared_screen.find_by_tag('rect').value_of_css_property('fill') == 'rgb(254, 248, 239)'


def test_theme_url(shared_screen: SharedScreen, test_route: str):  # pylint: disable=redefined-outer-name
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

    shared_screen.open('/')
    assert shared_screen.find_by_tag('rect').value_of_css_property('fill') == 'rgb(254, 248, 239)'


def test_click(shared_screen: SharedScreen):
    events = []

    @ui.page('/')
    def page():
        ui.echart({
            'legend': {
                'triggerEvent': True,
            },
            'radar': {
                'triggerEvent': True,
                'indicator': [{'name': name, 'max': 100} for name in ['A', 'B', 'C']],
            },
            'series': [{
                'type': 'radar',
                'data': [{'name': 'Test', 'value': [77.0, 50.0, 90.0]}],
                'animation': False,
            }],
        }, on_point_click=lambda e: events.append(('point', e)), on_click=lambda e: events.append(('component', e))) \
            .style('width: 200px; height: 200px')

    shared_screen.open('/')
    echart = shared_screen.find_by_tag('canvas')
    for x, y in [(20, 20), (0, 70), (60, 30)]:
        shared_screen.click_at_position(echart, x, y)
    shared_screen.wait(0.5)
    assert [(source, event.component_type, event.name) for source, event in events] == [
        ('point', 'series', 'Test'),
        ('component', 'series', 'Test'),
        ('component', 'legend', None),
        ('component', 'radar', 'C'),
    ]
