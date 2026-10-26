from nicegui import ui

from . import doc


@doc.demo(ui.uplot)
def main_demo() -> None:
    import math

    ui.uplot(
        options={
            'width': 600,
            'height': 300,
            'title': 'Sine wave',
            'scales': {'x': {'time': False}},
            'series': [
                {'label': 'x'},
                {'label': 'sin(x)', 'stroke': 'red'},
            ],
        },
        data=[
            [x / 10 for x in range(100)],
            [math.sin(x / 10) for x in range(100)],
        ],
    )


@doc.demo('Updating data and options', '''
    Assign new values to `chart.data` or `chart.options`, or modify them in place, to update the chart.
''')
def update_demo() -> None:
    from random import random

    chart = ui.uplot(
        options={'width': 600, 'height': 300, 'scales': {'x': {'time': False}},
                 'series': [{'label': 'x'}, {'label': 'y', 'stroke': 'blue'}]},
        data=[[0, 1, 2, 3], [1, 3, 2, 4]],
    )

    def update() -> None:
        chart.data = [[0, 1, 2, 3], [random(), random(), random(), random()]]

    ui.button('Update', on_click=update)


@doc.demo('Live updates with preserved zoom', '''
    While the x axis is zoomed or panned, data updates keep the current scales instead of refitting them to the new data.
    Try zooming into the chart by dragging across it while it keeps streaming, and double-click to zoom out again.
    Pass `keep_zoom=False` to always refit,
    or set `auto: False` for a scale in the options to never refit it.
''')
def live_demo() -> None:
    import math

    xs = list(range(100))
    ys = [math.sin(x / 10) for x in xs]
    chart = ui.uplot(
        options={'width': 600, 'height': 300, 'scales': {'x': {'time': False}},
                 'series': [{'label': 'x'}, {'label': 'value', 'stroke': 'green'}]},
        data=[xs, ys],
    )

    def update() -> None:
        xs.append(xs[-1] + 1)
        ys.append(math.sin(xs[-1] / 10))
        xs.pop(0)
        ys.pop(0)
        chart.data = [xs, ys]

    ui.timer(0.1, update)


@doc.demo('Sizing', '''
    The `width` and `height` in the options are optional: set them for a default size, or omit them to fill the parent.
    Either way the chart follows its element via a `ResizeObserver`, so you can size it with Tailwind classes or `.style()`.
    Note that `width` and `height` only apply when the chart is created;
    to resize it later, change the element's classes or style rather than the options.
''')
def sizing_demo() -> None:
    import math

    options = {'width': 600, 'height': 300, 'scales': {'x': {'time': False}},
               'series': [{'label': 'x'}, {'label': 'cos(x)', 'stroke': 'purple'}]}
    data = [[x / 10 for x in range(100)], [math.cos(x / 10) for x in range(100)]]

    ui.uplot(options, data)
    ui.uplot(options, data).classes('w-full h-40')


doc.reference(ui.uplot)
