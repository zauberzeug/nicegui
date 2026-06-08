from nicegui import ui

from . import doc


@doc.demo(ui.plotly)
def main_demo() -> None:
    import plotly.graph_objects as go

    fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    ui.plotly(fig).classes('w-full h-40')


@doc.demo('Dictionary interface', '''
    This demo shows how to use the declarative dictionary interface to create a plot.
    For plots with many traces and data points, this is more efficient than the object-oriented interface.
    The definition corresponds to the [JavaScript Plotly API](https://plotly.com/javascript/).
    Due to different defaults, the resulting plot may look slightly different from the same plot created with the object-oriented interface,
    but the functionality is the same.
''')
def plot_dict_interface():
    fig = {
        'data': [
            {
                'type': 'scatter',
                'name': 'Trace 1',
                'x': [1, 2, 3, 4],
                'y': [1, 2, 3, 2.5],
            },
            {
                'type': 'scatter',
                'name': 'Trace 2',
                'x': [1, 2, 3, 4],
                'y': [1.4, 1.8, 3.8, 3.2],
                'line': {'dash': 'dot', 'width': 3},
            },
        ],
        'layout': {
            'margin': {'l': 15, 'r': 0, 't': 0, 'b': 15},
            'plot_bgcolor': '#E5ECF6',
            'xaxis': {'gridcolor': 'white'},
            'yaxis': {'gridcolor': 'white'},
        },
    }
    ui.plotly(fig).classes('w-full h-40')


@doc.demo('Plot updates', '''
    This demo shows how to update the plot in real time.
    Click the button to add a new trace to the plot.
    To send the new plot to the browser, make sure to explicitly call `plot.update()` or `ui.update(plot)`.
''')
def plot_updates():
    from random import random

    import plotly.graph_objects as go

    fig = go.Figure()
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    plot = ui.plotly(fig).classes('w-full h-40')

    def add_trace():
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[random(), random(), random()]))
        plot.update()

    ui.button('Add trace', on_click=add_trace)


@doc.demo('Extending traces without re-sending the full figure', '''
    Calling `plot.update()` re-transmits the entire figure to the client.
    For live data, [`Plotly.extendTraces`](https://plotly.com/javascript/plotlyjs-function-reference/#plotlyextendtraces)
    appends points to existing traces with minimal traffic.
    Use `plot.run_plot_method('extendTraces', ...)` to call it directly,
    and mutate `figure['data']` on the server so the next `plot.update()` reflects the full state.
    Note the dict form of the figure (instead of `go.Figure`),
    so the trace's `x` and `y` stay mutable lists that can be appended to.

    *Added in version 3.13.0*
''')
def extending_traces():
    from random import random

    fig = {
        'data': [{'type': 'scatter', 'x': [], 'y': []}],
        'layout': {'margin': {'l': 30, 'r': 0, 't': 0, 'b': 30}},
    }
    plot = ui.plotly(fig).classes('w-full h-40')

    def add_point():
        t = len(fig['data'][0]['x'])
        y = random()
        fig['data'][0]['x'].append(t)
        fig['data'][0]['y'].append(y)
        plot.run_plot_method('extendTraces', {'x': [[t]], 'y': [[y]]}, [0])

    ui.button('Add point', on_click=add_point)


@doc.demo('Plot events', r'''
    This demo shows how to handle Plotly events.
    Try clicking on a data point to see the event data.

    Currently, the following events are supported:
    "plotly\_click",
    "plotly\_legendclick",
    "plotly\_selecting",
    "plotly\_selected",
    "plotly\_hover",
    "plotly\_unhover",
    "plotly\_legenddoubleclick",
    "plotly\_restyle",
    "plotly\_relayout",
    "plotly\_webglcontextlost",
    "plotly\_afterplot",
    "plotly\_autosize",
    "plotly\_deselect",
    "plotly\_doubleclick",
    "plotly\_redraw",
    "plotly\_animated".
    For more information, see the [Plotly documentation](https://plotly.com/javascript/plotlyjs-events/).
''')
def plot_events():
    import plotly.graph_objects as go

    fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    plot = ui.plotly(fig).classes('w-full h-40')
    plot.on('plotly_click', ui.notify)


@doc.demo('Large datasets', '''
    When plotting a large number of data points, pass NumPy arrays (or pandas Series) to Plotly rather than Python lists,
    and avoid converting them back with `.tolist()`.
    For NumPy arrays, Plotly uses a compact binary encoding (base64-encoded typed arrays)
    that makes the payload roughly half the size — far less data to transfer, parse and keep in memory —
    which is what avoids freezing the UI on large updates.
    This requires Plotly 6.0 or newer, where the binary encoding is the default.
''')
def large_datasets():
    import numpy as np
    import plotly.graph_objects as go

    x = np.linspace(0, 10, 100_000)
    y = np.sin(x) + np.random.normal(0, 0.1, x.size)
    fig = go.Figure(go.Scattergl(x=x, y=y, mode='markers', marker=dict(size=2)))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    ui.plotly(fig).classes('w-full h-40')


doc.reference(ui.plotly)
