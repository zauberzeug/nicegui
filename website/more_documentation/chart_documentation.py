from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    from random import random

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
        chart.options['series'][0]['data'][0] = random()
        chart.update()

    ui.button('Update', on_click=update)


def more() -> None:
    @text_demo('Chart with extra dependencies', '''
        To use a chart type that is not included in the default dependencies, you can specify extra dependencies.
        This demo shows a solid gauge chart.
    ''')
    def extra_dependencies() -> None:
        ui.chart({
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
