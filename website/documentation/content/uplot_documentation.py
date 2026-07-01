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
    ).classes('bg-white text-black')


@doc.demo('Updating data and options', '''
    uPlot data and options are bindable properties.
    Just assign a new value to `chart.data` or mutate `chart.options` to push an update to the client.
''')
def update_demo() -> None:
    from random import random

    chart = ui.uplot(
        options={'width': 600, 'height': 300, 'scales': {'x': {'time': False}},
                 'series': [{'label': 'x'}, {'label': 'y', 'stroke': 'blue'}]},
        data=[[0, 1, 2, 3], [1, 3, 2, 4]],
    ).classes('bg-white text-black')

    def update() -> None:
        chart.data = [[0, 1, 2, 3], [random(), random(), random(), random()]]

    ui.button('Update', on_click=update)


@doc.demo('Live updates with preserved zoom', '''
    With `scale_mode="preserve_zoom"` the chart keeps the user's current zoom/pan across data updates
    instead of rescaling to the full data range on every refresh.
    Try zooming into the chart by dragging across it while it keeps streaming.

    The available modes are `"reset"` (always rescale, the default),
    `"preserve_zoom"` (rescale only while not zoomed) and `"preserve_all"` (never rescale).
''')
def live_demo() -> None:
    import math

    xs = list(range(100))
    ys = [math.sin(x / 10) for x in xs]
    chart = ui.uplot(
        options={'width': 600, 'height': 300, 'scales': {'x': {'time': False}},
                 'series': [{'label': 'x'}, {'label': 'value', 'stroke': 'green'}]},
        data=[xs, ys],
        scale_mode='preserve_zoom',
    ).classes('bg-white text-black')

    def update() -> None:
        xs.append(xs[-1] + 1)
        ys.append(math.sin(xs[-1] / 10))
        xs.pop(0)
        ys.pop(0)
        chart.data = [xs, ys]

    ui.timer(0.1, update)


@doc.demo('Sizing', '''
    The `width` and `height` in the options are optional: set them for a default size, or omit them
    to fill the parent. Either way the chart follows its element via a `ResizeObserver`,
    so you can size it with Tailwind classes or `.style()`.
''')
def sizing_demo() -> None:
    import math

    options = {'width': 600, 'height': 300, 'scales': {'x': {'time': False}},
               'series': [{'label': 'x'}, {'label': 'cos(x)', 'stroke': 'purple'}]}
    data = [[x / 10 for x in range(100)], [math.cos(x / 10) for x in range(100)]]

    ui.uplot(options, data).classes('bg-white text-black')
    ui.uplot(options, data).classes('w-full h-40 bg-white text-black')


doc.reference(ui.uplot)
