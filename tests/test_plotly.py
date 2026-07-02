import base64
from datetime import datetime, timedelta

import numpy as np
import plotly.graph_objects as go

from nicegui import ui
from nicegui.testing import Screen, User


def test_plotly(screen: Screen):
    @ui.page('/')
    def page():
        fig = go.Figure(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name='Trace 1'))
        fig.update_layout(title='Test Figure')
        plot = ui.plotly(fig)

        ui.button('Add trace', on_click=lambda: (
            # test NumPy array support for value arrays
            fig.add_trace(go.Scatter(x=np.array([0, 1, 2]), y=np.array([2, 1, 0]), name='Trace 2')),
            plot.update()
        ))

    screen.open('/')
    screen.should_contain('Test Figure')

    screen.click('Add trace')
    screen.should_contain('Trace 1')
    screen.should_contain('Trace 2')


def test_replace_plotly(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.plotly(go.Figure(go.Scatter(x=[1], y=[1], text=['A'], mode='text')))

        def replace():
            with container.clear():
                ui.plotly(go.Figure(go.Scatter(x=[1], y=[1], text=['B'], mode='text')))
        ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find_by_tag('text').text == 'A'

    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('text').text == 'B'


def test_create_dynamically(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('Create', on_click=lambda: ui.plotly(go.Figure(go.Scatter(x=[], y=[]))))

    screen.open('/')
    screen.click('Create')
    assert screen.find_by_tag('svg')


def test_run_plot_method(screen: Screen):
    @ui.page('/')
    def page():
        plot = ui.plotly({'data': [{'type': 'scatter', 'mode': 'text', 'x': [1], 'y': [1], 'text': ['Alpha']}]})
        button = ui.button('Extend')
        button.on_click(lambda: plot.run_plot_method('extendTraces', {'x': [[2]], 'y': [[2]], 'text': [['Beta']]}, [0]))

    screen.open('/')
    screen.should_contain('Alpha')
    screen.should_not_contain('Beta')

    screen.click('Extend')
    screen.should_contain('Beta')
    screen.should_contain('Alpha')


def test_run_plot_method_awaited(screen: Screen):
    @ui.page('/')
    def page():
        plot = ui.plotly(go.Figure(go.Scatter(x=[1, 2, 3], y=[1, 2, 3])))

        async def extend():
            # functions like extendTraces resolve to the graph element; awaiting must not time out
            result = await plot.run_plot_method('extendTraces', {'y': [[4]]}, [0])
            ui.label(f'result: {result!r}')
        ui.button('Extend', on_click=extend)

    screen.open('/')
    screen.click('Extend')
    screen.should_contain('result: None')


def _number_of_points(values) -> int:
    """Length of a serialized value array (plain list or Plotly's binary ``bdata`` encoding of NumPy arrays)."""
    if isinstance(values, dict) and 'bdata' in values:
        return len(base64.b64decode(values['bdata'])) // np.dtype(values['dtype']).itemsize
    return len(values)


async def test_resampling_limits_transmitted_points(user: User):
    plots: dict[str, ui.plotly] = {}

    @ui.page('/')
    def page():
        x = np.arange(10_000)
        y = np.sin(x / 100)
        plots['figure'] = ui.plotly(go.Figure(go.Scattergl(x=x, y=y, mode='lines')), n_samples=100)
        plots['dict'] = ui.plotly({'data': [{'type': 'scatter', 'x': x.tolist(), 'y': y.tolist()}]}, n_samples=100)

    await user.open('/')
    for plot in plots.values():
        data = plot._props['options']['data']  # pylint: disable=protected-access
        assert _number_of_points(data[0]['x']) == 100, 'only n_samples points should be sent to the client'
        assert _number_of_points(data[0]['y']) == 100
        assert len(next(iter(plot._hf_data.values())).x) == 10_000, \
            'the full dataset should be retained on the server'  # pylint: disable=protected-access


async def test_resampling_on_zoom_and_reset(user: User):
    plots: list[ui.plotly] = []

    @ui.page('/')
    def page():
        x = np.arange(10_000)
        y = np.sin(x / 100)
        plots.append(ui.plotly({'data': [{'type': 'scatter', 'x': x.tolist(), 'y': y.tolist()}]}, n_samples=100))

    await user.open('/')

    def transmitted_x() -> list:
        return plots[0]._props['options']['data'][0]['x']  # pylint: disable=protected-access

    user.find(ui.plotly).trigger('plotly_relayout', args={'xaxis.range[0]': 1000, 'xaxis.range[1]': 1050})
    assert transmitted_x() == list(range(1000, 1051)), 'zooming below n_samples points should show full resolution'

    user.find(ui.plotly).trigger('plotly_relayout', args={'xaxis.range[0]': 0, 'xaxis.range[1]': 5000})
    xs = transmitted_x()
    assert len(xs) == 100, 'zoomed range with more than n_samples points should be resampled'
    assert xs[0] == 0 and xs[-1] == 5000, 'resampling should keep the first and last point of the visible range'

    user.find(ui.plotly).trigger('plotly_relayout', args={'xaxis.autorange': True})
    xs = transmitted_x()
    assert len(xs) == 100


async def test_resampling_preserves_datetime_x(user: User):
    plots: list[ui.plotly] = []

    @ui.page('/')
    def page():
        start = datetime(2020, 1, 1)
        x = [start + timedelta(hours=i) for i in range(10_000)]  # native datetimes, the common time-axis form
        y = np.sin(np.arange(10_000) / 100).tolist()
        plots.append(ui.plotly({'data': [{'type': 'scatter', 'x': x, 'y': y}]}, n_samples=100))

    await user.open('/')  # must not raise: datetime x used to crash the float64 coercion
    xs = plots[0]._props['options']['data'][0]['x']  # pylint: disable=protected-access
    assert len(xs) == 100
    assert all(isinstance(value, datetime) for value in xs), 'datetime x must survive resampling, not become floats'
    assert xs[0] == datetime(2020, 1, 1) and xs[-1] == datetime(2020, 1, 1) + timedelta(hours=9_999)


async def test_resampling_does_not_mutate_caller_figure(user: User):
    x = np.arange(10_000)
    y = np.sin(x / 100)
    dict_figure = {'data': [{'type': 'scatter', 'x': x.tolist(), 'y': y.tolist()}]}
    go_figure = go.Figure(go.Scattergl(x=x, y=y, mode='lines'))

    @ui.page('/')
    def page():
        ui.plotly(dict_figure, n_samples=100)
        ui.plotly(go_figure, n_samples=100)

    await user.open('/')
    assert len(dict_figure['data'][0]['x']) == 10_000, 'the caller-provided dict figure must not be mutated'
    assert len(go_figure.data[0].x) == 10_000, 'the caller-provided go.Figure must not be mutated'


async def test_resampling_handles_tiny_n_samples(user: User):
    plots: list[ui.plotly] = []

    @ui.page('/')
    def page():
        x = np.arange(10_000)
        y = np.sin(x / 100)
        plots.append(ui.plotly({'data': [{'type': 'scatter', 'x': x.tolist(), 'y': y.tolist()}]}, n_samples=2))

    await user.open('/')  # must not raise: tsdownsample panics for n_out < 3, so it is guarded
    xs = plots[0]._props['options']['data'][0]['x']  # pylint: disable=protected-access
    assert xs == [0, 9999], 'n_samples below 3 should keep the endpoints'


async def test_resampling_on_combined_range_key(user: User):
    plots: list[ui.plotly] = []

    @ui.page('/')
    def page():
        x = np.arange(10_000)
        y = np.sin(x / 100)
        plots.append(ui.plotly({'data': [{'type': 'scatter', 'x': x.tolist(), 'y': y.tolist()}]}, n_samples=100))

    await user.open('/')
    # some Plotly relayout payloads use the combined "xaxis.range" list instead of split range[0]/range[1] keys
    user.find(ui.plotly).trigger('plotly_relayout', args={'xaxis.range': [1000, 1050]})
    xs = plots[0]._props['options']['data'][0]['x']  # pylint: disable=protected-access
    assert xs == list(range(1000, 1051)), 'the combined range key should drive resampling'


async def test_resampling_numeric_string_and_missing_x(user: User):
    plots: dict[str, ui.plotly] = {}

    @ui.page('/')
    def page():
        y = np.sin(np.arange(10_000) / 100).tolist()
        # numeric strings must be treated as numbers, not parsed as calendar years
        plots['strings'] = ui.plotly({'data': [{'type': 'scatter', 'x': [str(i) for i in range(10_000)], 'y': y}]},
                                     n_samples=100)
        # None entries in x must be dropped, not kept as a bogus timestamp
        x_gap = [*range(5_000), None, *range(5_001, 10_000)]
        plots['gap'] = ui.plotly({'data': [{'type': 'scatter', 'x': x_gap, 'y': y}]}, n_samples=100)

    await user.open('/')
    xs = plots['strings']._props['options']['data'][0]['x']  # pylint: disable=protected-access
    assert len(xs) == 100 and xs[0] == '0' and xs[-1] == '9999', 'numeric strings should resample as numbers'
    gap_xs = plots['gap']._props['options']['data'][0]['x']  # pylint: disable=protected-access
    assert None not in gap_xs, 'missing (None) x values should be dropped, not kept as a sentinel'
