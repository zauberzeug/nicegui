#!/usr/bin/env python3
"""Demonstrates embedding altair charts in NiceGUI.

This shows how to embed altair charts in NiceGUI, and how to synchronize
NiceGUI elements with charts using ``.bind_*`` (chart -> NiceGUI) and ``on_*``
callbacks (NiceGUI -> chart).
"""

import altair as alt
import numpy as np
import pandas as pd

from nicegui import ui


def create_altair_chart() -> alt.Chart:
    """Create simple altair chart with slider-based coloring

    Refer to:
    https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html#accessing-variable-params
    """
    rand = np.random.RandomState(42)

    df = pd.DataFrame({
        'xval': range(100),
        'yval': rand.randn(100).cumsum()
    })

    slider = alt.binding_range(min=0, max=100, step=1)
    cutoff = alt.param(name='cutoff', bind=slider, value=50)

    chart = alt.Chart(df).mark_point().encode(
        x='xval',
        y='yval',
        color=alt.condition(
            alt.datum.xval < cutoff,
            alt.value('red'), alt.value('blue')
        )
    ).add_params(
        cutoff
    )
    return chart


@ui.page('/')
def page():
    # Example 1: getting started example from altair documentation
    # https://altair-viz.github.io/getting_started/starting.html#customizing-your-visualization
    with ui.card().classes('min-w-200px max-w-300px'):
        ui.label('Static altair chart').classes('text-xl font-bold')

        data = pd.DataFrame({'a': list('CCCDDDEEE'), 'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})
        chart = alt.Chart(data).mark_bar(color='firebrick').encode(
            alt.Y('a').title('category'),
            alt.X('average(b)').title('avg(b) by category')
        )
        ui.altair(chart)

    # Example 2: altair chart widget with slider synchronized between nicegui & altair
    # This is the JupyterChart variable params example from the altair documentation:
    # https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html#accessing-variable-params
    with ui.card().classes('min-w-200px max-w-300px'):
        ui.label('Synchronized altair and nicegui sliders').classes('text-xl font-bold')
        # jchart = AltairChart(create_altair_chart())
        chart = create_altair_chart()
        widget = ui.altair(chart, throttle=0.5)

        def update_cutoff(change):
            # NOTE: as of altair v5.5, there is a JavaScript side bug in altair.JupyterChart
            # that causes this callback to fail when accessing .changed (only supported in Jupyter):
            # https://github.com/vega/altair/issues/3868
            widget._widget.params.cutoff = change.value
        slider = ui.slider(
            min=0, max=100, value=widget._widget.params.cutoff, on_change=update_cutoff, throttle=0.2
        ).bind_value_from(widget._widget, '_params', backward=lambda p: p['cutoff'])
        ui.label().bind_text_from(slider, 'value', backward=lambda c: f'Cutoff is {c}')


ui.run(show=False)
