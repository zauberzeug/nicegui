from nicegui import ui


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


def more() -> None:
    @text_demo('Chart with clickable points', '''
        You can register a callback for an event when a series point is clicked.
    ''')
    def click() -> None:
        echart = ui.echart({
            'xAxis': {'type': 'category'},
            'yAxis': {'type': 'value', 'data': 'A', 'inverse': True},
            'legend': {'textStyle': {'color': 'gray'}},
            'series': [
                {'type': 'line', 'name': 'Alpha', 'data': [20, 10, 30, 50, 40, 30]},
            ],
        },
        on_point_click=lambda e: ui.notify(f'Click {e}')
        ).classes('w-full h-64')
