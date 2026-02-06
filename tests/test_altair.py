import altair as alt
import pandas as pd

from nicegui import ui
from nicegui.testing import SharedScreen


def test_construction(shared_screen: SharedScreen):
    def chart():
        df = pd.DataFrame([{'x': 1, 'y': 3}, {'x': 2, 'y': 5}, {'x': 3, 'y': 4}, {'x': 4, 'y': 6}])
        return alt.Chart(df).mark_point().encode(alt.X('x:Q'), alt.Y('y:Q'))

    @ui.page('/')
    def page():
        ui.altair(chart()).classes('my-chart')
        ui.altair(alt.layer(chart(), chart())).classes('my-chart')
        ui.altair(alt.concat(chart(), chart())).classes('my-chart')
        ui.altair(chart().facet('x')).classes('my-chart')
        ui.altair(alt.hconcat(chart(), chart())).classes('my-chart')
        ui.altair(alt.vconcat(chart(), chart())).classes('my-chart')
        ui.altair(chart().repeat(column=['x', 'y'], row=['x', 'y'])).classes('my-chart')

    shared_screen.open('/')
    assert len(shared_screen.find_all_by_class('my-chart')) == 7
