from nicegui import optional_features, ui

from ..tools import load_demo


def content() -> None:
    load_demo(ui.table)
    load_demo(ui.aggrid)
    if optional_features.has('highcharts'):
        load_demo(ui.highchart)
    load_demo(ui.echart)
    if optional_features.has('matplotlib'):
        load_demo(ui.pyplot)
        load_demo(ui.line_plot)
    if optional_features.has('plotly'):
        load_demo(ui.plotly)
    load_demo(ui.linear_progress)
    load_demo(ui.circular_progress)
    load_demo(ui.spinner)
    load_demo(ui.scene)
    load_demo(ui.tree)
    load_demo(ui.log)
    load_demo(ui.editor)
    load_demo(ui.code)
    load_demo(ui.json_editor)
