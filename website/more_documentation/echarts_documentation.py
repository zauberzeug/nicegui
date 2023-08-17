from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    from random import random

    echarts = ui.echarts({
        'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},
        'xAxis': {'type': 'value'},
        'legend': {'show': True, 'textStyle': {'color': '#777'}},
        'series': [
            {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},
            {'type': 'bar', 'name': 'Beta', 'data': [0.3, 0.4]},
        ]}).classes('w-full h-64')

    def update():
        echarts.options["series"][0]["data"][0] = random()
        echarts.update()

    ui.button("Update", on_click=update)
    ui.run()


def more() -> None:
    pass
