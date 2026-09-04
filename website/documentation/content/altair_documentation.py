from nicegui import ui

from . import doc


@doc.demo(ui.altair)
def main_demo() -> None:
    import altair as alt
    from altair.datasets import data

    cars = data.cars()

    chart = alt.Chart(cars).mark_point() \
        .encode(x='Horsepower', y='Miles_per_Gallon', color='Origin') \
        .interactive()

    ui.altair(chart)


@doc.demo('Interactive charts', '''
    Altair charts can be made interactive by adding parameters.
    This demo shows how to add a slider to control the color of the points.
''')
def interactive_altair() -> None:
    import altair as alt
    import numpy as np
    import pandas as pd

    df = pd.DataFrame({'x': range(100), 'y': np.random.randn(100).cumsum()})

    slider = alt.binding_range(min=0, max=100, step=1)
    cutoff = alt.param(name='cutoff', bind=slider, value=50)
    color = alt.condition(alt.datum.x < cutoff, alt.value('red'), alt.value('blue'))

    chart = alt.Chart(df).mark_point() \
        .encode(x='x', y='y', color=color) \
        .add_params(cutoff)

    ui.altair(chart)


doc.reference(ui.altair)
