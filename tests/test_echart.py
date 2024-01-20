from pyecharts import options
from pyecharts.charts import Bar
from pyecharts.commons import utils

from nicegui import ui
from nicegui.testing import Screen


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



def test_create_from_pyecharts(screen: Screen):
    xaxis_formatter = r'(val, idx) => `x for ${val}`'
    yaxis_formatter = r'(val, idx) => `${val} kg`'
    get_options_js = "echarts.getInstanceByDom(document.querySelector('.nicegui-echart')).getOption()"

    ui.echart.from_pyecharts(
        Bar()
        .add_xaxis(['A', 'B', 'C'])
        .add_yaxis('series A', [0.1,0.2,0.3],)
        .set_global_opts(
            xaxis_opts=options.AxisOpts(axislabel_opts={':formatter': xaxis_formatter}),
            yaxis_opts=options.AxisOpts(axislabel_opts={'formatter': utils.JsCode(yaxis_formatter)}),
        )
    )
    
    label = ui.label('')

    async def get_xAxis_formatter():
        type_str,formatter= await ui.run_javascript(f"const fm={get_options_js}.xAxis[0].axisLabel.formatter;[typeof fm,fm.toString()]")
        label.set_text(f"xAxis formatter is {type_str}: {formatter}")
    ui.button('Get xAxis formatter', on_click=get_xAxis_formatter)

    async def get_yAxis_formatter():
        type_str,formatter= await ui.run_javascript(f"const fm={get_options_js}.yAxis[0].axisLabel.formatter;[typeof fm,fm.toString()]")
        label.set_text(f"yAxis formatter is {type_str}: {formatter}")
    ui.button('Get yAxis formatter', on_click=get_yAxis_formatter)

    screen.open('/')
    screen.click('Get xAxis formatter')
    screen.should_contain(f"formatter is function: {xaxis_formatter}")

    screen.click('Get yAxis formatter')
    screen.should_contain(f"formatter is function: {yaxis_formatter}")
