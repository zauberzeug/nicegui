#!/usr/bin/env python3
"""Demonstrates embedding anywidget widgets in NiceGUI.

This shows how to embed anywidget widgets in NiceGUI, and how to synchronize
NiceGUI elements with widgets using ``.bind_*`` (widget -> NiceGUI) and ``on_*``
callbacks (NiceGUI -> widget).

The example shows how to embed a counter widget and an altair chart widget
from the getting started examples in anywidget and altair.
"""

import anywidget
import traitlets

from nicegui import ui


class CounterWidget(anywidget.AnyWidget):
    """Baseline anywidget example"""
    _esm = '''
    function render({ model, el }) {
      let button = document.createElement("button");
      button.innerHTML = `anywidget count is ${model.get("value")}`;
      button.addEventListener("click", () => {
        model.set("value", model.get("value") + 1);
        model.save_changes();
      });
      model.on("change:value", () => {
        button.innerHTML = `anywidget count is ${model.get("value")}`;
      });
      el.classList.add("counter-widget");
      el.appendChild(button);
    }
    export default { render };
    '''
    _css = '''
    .counter-widget button { color: white; font-size: 1.75rem; background-color: #ea580c; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; }
    .counter-widget button:hover { background-color: #9a3412; }
    '''
    value = traitlets.Int(0).tag(sync=True)


def create_altair_chart():
    """Create simple altair chart with slider-based coloring

    Refer to:
    https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html#accessing-variable-params
    """
    import altair as alt
    import numpy as np
    import pandas as pd

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
    return alt.JupyterChart(chart)


@ui.page('/')
def page():
    with ui.row():
        with ui.column():
            # Example 1: counter widget synchronized with nicegui & anywidget
            with ui.card().classes('min-w-200px max-w-300px'):
                ui.label('Synchronized anywidget and nicegui buttons').classes('text-xl font-bold')
                ui.markdown('''
                            This is the getting started example from the
                            [`anywidget` documentation](https://anywidget.dev/en/getting-started/).

                            `anywidget` gives us a way to write to bridge arbitrary JavaScript
                            libraries with Python with compatibility for multiple frontends (such as Jupyter/Marimo).

                            We can synchronize `anywidget` and NiceGUI state in python using a mix of
                            `traitlets` callbacks and NiceGUI's `bind_*` methods.
                            ''')
                counter = CounterWidget(value=42)
                ui.anywidget(counter)

                def increment_counter():
                    counter.value += 1
                ui.button(
                    f'NiceGUI count is {counter.value}', on_click=increment_counter
                ).bind_text_from(counter, 'value', backward=lambda c: f'NiceGUI count is {c}')

            # Example 2: altair chart widget with slider synchronized between nicegui & altair
            with ui.card().classes('min-w-200px max-w-300px'):
                ui.label('Synchronized altair and nicegui sliders').classes('text-xl font-bold')

                ui.markdown('''
                            This is the JupyterChart variable params example from the
                            [`altair` documentation](https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html#accessing-variable-params).

                            *Note: In `altair<=5.5`, the nicegui -> altair slider synchronization might
                            not work due to
                            [this bug in `altair.JupyterChart`.](https://github.com/vega/altair/issues/3868)
                            ''')

                # jchart = AltairChart(create_altair_chart())
                jchart = create_altair_chart()
                ui.anywidget(jchart, throttle=0.5)

                def update_cutoff(change):
                    # NOTE: as of altair v5.5, there is a JavaScript side bug in altair.JupyterChart
                    # that causes this callback to fail when accessing .changed (only supported in Jupyter):
                    # https://github.com/vega/altair/issues/3868
                    jchart.params.cutoff = change.value
                slider = ui.slider(
                    min=0, max=100, value=jchart.params.cutoff, on_change=update_cutoff, throttle=0.2
                ).bind_value_from(jchart, '_params', backward=lambda p: p['cutoff'])
                ui.label().bind_text_from(slider, 'value', backward=lambda c: f'Cutoff is {c}')


ui.run(show=False)
