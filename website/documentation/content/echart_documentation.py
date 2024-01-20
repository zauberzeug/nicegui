from nicegui import ui

from . import doc


@doc.demo(ui.echart)
def main_demo() -> None:
    from random import random

    echart = ui.echart({
        'xAxis': {'type': 'value'},
        'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},
        'legend': {'textStyle': {'color': 'gray'}},
        'series': [
            {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},
            {'type': 'bar', 'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    })

    def update():
        echart.options['series'][0]['data'][0] = random()
        echart.update()

    ui.button('Update', on_click=update)


@doc.demo('EChart with clickable points', '''
    You can register a callback for an event when a series point is clicked.
''')
def clickable_points() -> None:
    ui.echart({
        'xAxis': {'type': 'category'},
        'yAxis': {'type': 'value'},
        'series': [{'type': 'line', 'data': [20, 10, 30, 50, 40, 30]}],
    }, on_point_click=ui.notify)


@doc.demo('EChart with dynamic properties', '''
    Dynamic properties can be passed to chart elements to customize them such as apply an axis label format.
    To make a property dynamic, prefix a colon ":" to the property name.
''')
def dynamic_properties() -> None:
    ui.echart({
        'xAxis': {'type': 'category'},
        'yAxis': {'axisLabel': {':formatter': 'value => "$" + value'}},
        'series': [{'type': 'line', 'data': [5, 8, 13, 21, 34, 55]}],
    })

@doc.demo('EChart from pyecharts', '''
    You can create a echart from pyecharts using the `from_pyecharts` method. 
    This method takes a pyecharts chart object as input and returns a echart.
''')
def echart_from_pyecharts_demo():
    from pyecharts import options
    from pyecharts.charts import Bar
    from pyecharts.commons import utils

    ui.echart.from_pyecharts(
        Bar()
        .add_xaxis(['A', 'B', 'C'])
        .add_yaxis('series A', [0.1,0.2,0.3],)
        .set_global_opts(
            xaxis_opts=options.AxisOpts(axislabel_opts={':formatter': r'(val, idx) => `x for ${val}`'}),
            yaxis_opts=options.AxisOpts(axislabel_opts={'formatter': utils.JsCode(r'(val, idx) => `${val} kg`')}),
        )
    )


@doc.demo('Run methods', '''
    You can run methods of the EChart instance using the `run_chart_method` method.
    This demo shows how to show and hide the loading animation, how to get the current width of the chart,
    and how to add tooltips with a custom formatter.

    The colon ":" in front of the method name "setOption" indicates that the argument is a JavaScript expression
    that is evaluated on the client before it is passed to the method.
''')
def methods_demo() -> None:
    echart = ui.echart({
        'xAxis': {'type': 'category', 'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']},
        'yAxis': {'type': 'value'},
        'series': [{'type': 'line', 'data': [150, 230, 224, 218, 135]}],
    })

    ui.button('Show Loading', on_click=lambda: echart.run_chart_method('showLoading'))
    ui.button('Hide Loading', on_click=lambda: echart.run_chart_method('hideLoading'))

    async def get_width():
        width = await echart.run_chart_method('getWidth')
        ui.notify(f'Width: {width}')
    ui.button('Get Width', on_click=get_width)

    ui.button('Set Tooltip', on_click=lambda: echart.run_chart_method(
        ':setOption', r'{tooltip: {formatter: params => "$" + params.value}}',
    ))


doc.reference(ui.echart)
