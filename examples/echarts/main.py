from random import random

from nicegui import ui

option = {"xAxis": {"type": "value"}, "yAxis": {"type": "value"}, "series": [{"data": [[0, 0]], "type": "line"}]}

echarts = ui.echarts(option).style("min-width: 100%").style("min-height: 400px")
point = 1


def update():
    global point
    echarts.options["series"][0]["data"].append([point, random()])
    point = point + 1
    echarts.update()


ui.button("Update", on_click=update)
ui.run()
