from nicegui import ui

from . import doc


@doc.demo(ui.uplot)
def main_demo() -> None:
    import math

    ui.uplot({
        'title': 'Sine wave',
        'scales': {'x': {'time': False}},
        'series': [
            {'label': 'x'},
            {'label': 'sin(x)', 'stroke': 'red'},
        ],
    }, [
        [x / 10 for x in range(100)],
        [math.sin(x / 10) for x in range(100)],
    ])


@doc.demo('Updating data and options', '''
    Assign new values to `chart.data` or `chart.options`, or modify them in place, to update the chart.
''')
def update_demo() -> None:
    import random

    chart = ui.uplot({
        'scales': {'x': {'time': False}},
        'series': [
            {'label': 'x'},
            {'label': 'y', 'stroke': 'blue'},
        ],
    }, [
        [0, 1, 2, 3, 4, 5],
        [3, 1, 4, 1, 5, 9],
    ])

    ui.button('Shuffle', on_click=lambda: random.shuffle(chart.data[1]))


@doc.demo('Live updates with preserved zoom', '''
    While the x axis is zoomed or panned, data updates keep the current scales instead of refitting them to the new data.
    Try zooming into the chart by dragging across it while it keeps streaming, and double-click to zoom out again.
    Pass `keep_zoom=False` to always refit,
    or set `auto: False` for a scale in the options to never refit it.
''')
def live_demo() -> None:
    import time
    import numpy as np

    chart = ui.uplot({'series': [{}, {'label': 'value', 'stroke': 'green'}]}, [[], []])

    def update() -> None:
        t = np.linspace(time.time() - 10, time.time(), 100)
        chart.data = [t, np.sin(t)]

    ui.timer(0.1, update)


doc.reference(ui.uplot)
