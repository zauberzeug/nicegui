from nicegui import ui

from . import doc


@doc.demo(ui.highchart)
def main_demo() -> None:
    from random import random

    chart = ui.highchart({
        'title': False,
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['A', 'B']},
        'series': [
            {'name': 'Alpha', 'data': [0.1, 0.2]},
            {'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    }).classes('w-full h-64')

    def update():
        chart.options['series'][0]['data'][0] = random()

    ui.button('Update', on_click=update)


@doc.demo('Chart with extra dependencies', '''
    To use a chart type that is not included in the default dependencies, you can specify extra dependencies.
    This demo shows a solid gauge chart.
''')
def extra_dependencies() -> None:
    ui.highchart({
        'title': False,
        'chart': {'type': 'solidgauge'},
        'yAxis': {
            'min': 0,
            'max': 1,
        },
        'series': [
            {'data': [0.42]},
        ],
    }, extras=['solid-gauge']).classes('w-full h-64')


@doc.demo('Chart with draggable points', '''
    This chart allows dragging the series points.
    You can register callbacks for the following events:

    - `on_point_click`: called when a point is clicked
    - `on_point_drag_start`: called when a point drag starts
    - `on_point_drag`: called when a point is dragged
    - `on_point_drop`: called when a point is dropped
''')
def drag() -> None:
    ui.highchart(
        {
            'title': False,
            'plotOptions': {
                'series': {
                    'stickyTracking': False,
                    'dragDrop': {'draggableY': True, 'dragPrecisionY': 1},
                },
            },
            'series': [
                {'name': 'A', 'data': [[20, 10], [30, 20], [40, 30]]},
                {'name': 'B', 'data': [[50, 40], [60, 50], [70, 60]]},
            ],
        },
        extras=['draggable-points'],
        on_point_click=lambda e: ui.notify(f'Click: {e}'),
        on_point_drag_start=lambda e: ui.notify(f'Drag start: {e}'),
        on_point_drop=lambda e: ui.notify(f'Drop: {e}')
    ).classes('w-full h-64')


doc.reference(ui.highchart)
