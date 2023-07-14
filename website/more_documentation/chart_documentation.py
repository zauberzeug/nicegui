from nicegui import ui


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
