from nicegui import ui

from . import doc


@doc.demo(ui.altair)
def main_demo() -> None:
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

    ui.altair(chart, throttle=0.5)

    ui.run()


doc.reference(ui.altair)
