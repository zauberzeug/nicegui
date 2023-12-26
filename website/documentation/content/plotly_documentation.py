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


@doc.demo('Plot events', '''
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


doc.reference(ui.plotly)
