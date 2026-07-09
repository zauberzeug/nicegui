from __future__ import annotations

import copy
from contextlib import suppress

import numpy as np

from ... import optional_features
from ...awaitable_response import AwaitableResponse
from ...element import Element
from ...events import GenericEventArguments
from ._resampling import Downsampler, HFTraceData, as_array, create_downsampler, to_numeric

with suppress(ImportError):
    import plotly.graph_objects as go
    optional_features.register('plotly')


class Plotly(Element, component='plotly.js', esm={'nicegui-plotly': 'dist'}):

    def __init__(self, figure: dict | go.Figure, *, n_samples: int | None = None) -> None:
        """Plotly Element

        Renders a Plotly chart.
        There are two ways to pass a Plotly figure for rendering, see parameter `figure`:

        * Pass a `go.Figure` object, see https://plotly.com/python/

        * Pass a Python `dict` object with keys `data`, `layout`, `config` (optional), see https://plotly.com/javascript/

        For best performance, use the declarative `dict` approach for creating a Plotly chart.

        :param figure: Plotly figure to be rendered. Can be either a `go.Figure` instance, or
                       a `dict` object with keys `data`, `layout`, `config` (optional).
        :param n_samples: If set, enables dynamic resampling for large datasets.
                          Only the specified number of samples will be sent to the client,
                          with automatic resampling on zoom/pan using the LTTB algorithm.
                          Only "scatter" and "scattergl" traces with numeric or datetime x are resampled,
                          and only the primary x-axis is tracked (subplots are not resampled yet).
                          Data with unsorted x is sorted by x before resampling, which reorders line traces.
                          For better performance, install ``pip install nicegui[tsdownsample]``.
                          *Added in version 3.14.0*
        """
        super().__init__()

        self.figure = figure
        self._n_samples = n_samples
        self._hf_data: dict[str, HFTraceData] = {}
        self._downsampler: Downsampler | None = None

        if n_samples:
            self.figure = copy.deepcopy(figure)  # resampling rewrites trace data, so never mutate the caller's figure
            self._downsampler = create_downsampler()
            self._extract_hf_data()
            self._apply_resampling()
            self.on('plotly_relayout', self._handle_relayout)

        self.update()
        self._classes.append('js-plotly-plot')
        self._update_method = 'update'

    def _get_figure_data(self) -> list[dict]:
        """Get the figure data as a list of trace dicts."""
        if optional_features.has('plotly') and isinstance(self.figure, go.Figure):
            return list(self.figure.data)
        if isinstance(self.figure, dict):
            return self.figure.get('data', [])
        return []

    def _extract_hf_data(self) -> None:
        """Extract and store high-frequency data from all scatter traces."""
        traces = self._get_figure_data()
        for idx, trace in enumerate(traces):
            trace_dict = trace.to_plotly_json() if hasattr(trace, 'to_plotly_json') else trace
            if trace_dict.get('type', 'scatter') not in ('scatter', 'scattergl'):
                continue  # NOTE: Plotly has no "line" trace type; line charts are scatter traces with mode='lines'

            x = trace_dict.get('x')
            y = trace_dict.get('y')
            if x is None or y is None:
                continue

            # Keep the original values (to preserve datetime/integer dtypes) alongside float64 views for the algorithm.
            x_arr = as_array(x)
            y_arr = as_array(y)
            x_num = to_numeric(x_arr)
            y_num = to_numeric(y_arr)
            if x_num is None or y_num is None:
                continue  # non-numeric, non-datetime data cannot be resampled; leave the trace untouched

            # Remove NaN values (tsdownsample requires no NaNs in x-data and handles y-data poorly)
            valid_mask = ~(np.isnan(x_num) | np.isnan(y_num))
            if not valid_mask.all():
                x_arr, y_arr, x_num, y_num = x_arr[valid_mask], y_arr[valid_mask], x_num[valid_mask], y_num[valid_mask]

            if len(x_num) < (self._n_samples or 0):
                continue

            # tsdownsample requires x-data to be monotonically increasing (sorted)
            if not np.all(x_num[:-1] <= x_num[1:]):
                sort_indices = np.argsort(x_num)
                x_arr, y_arr, x_num, y_num = x_arr[sort_indices], y_arr[sort_indices], x_num[sort_indices], y_num[sort_indices]

            uid = trace_dict.get('uid') or f'trace_{idx}'
            self._hf_data[uid] = HFTraceData(x=x_arr, y=y_arr, x_num=x_num, y_num=y_num, trace_idx=idx)

    def _apply_resampling(self, x_range: tuple[float, float] | None = None) -> None:
        """Apply resampling to all stored high-frequency traces."""
        n_samples = self._n_samples or 0
        if not self._downsampler or not n_samples:
            return

        for hf in self._hf_data.values():
            if x_range is not None:
                indices_in_range = np.where((hf.x_num >= x_range[0]) & (hf.x_num <= x_range[1]))[0]
                if len(indices_in_range) == 0:
                    continue
                start_idx, end_idx = int(indices_in_range[0]), int(indices_in_range[-1]) + 1
            else:
                start_idx, end_idx = 0, len(hf.x_num)

            slice_len = end_idx - start_idx
            n_out = min(n_samples, slice_len)

            indices: np.ndarray  # annotate so branch assignments don't clash on NumPy's shape-typed dtype
            if slice_len <= n_out:
                indices = np.arange(slice_len, dtype=np.uint64)
            elif n_out < 3:
                # tsdownsample panics for n_out < 3; both implementations just keep the endpoints here.
                indices = np.array([0, slice_len - 1][:n_out], dtype=np.uint64)
            else:
                indices = self._downsampler.downsample(hf.x_num[start_idx:end_idx],
                                                       hf.y_num[start_idx:end_idx], n_out=n_out)

            # Index the original (dtype-preserving) arrays so datetime/integer x survives the round-trip.
            self._update_trace_data(hf.trace_idx, hf.x[start_idx:end_idx][indices], hf.y[start_idx:end_idx][indices])

    def _update_trace_data(self, trace_idx: int, x: np.ndarray, y: np.ndarray) -> None:
        """Update a trace's x and y data in the figure."""
        if optional_features.has('plotly') and isinstance(self.figure, go.Figure):
            self.figure.data[trace_idx].x = x
            self.figure.data[trace_idx].y = y
        elif isinstance(self.figure, dict):
            self.figure['data'][trace_idx]['x'] = x.tolist()
            self.figure['data'][trace_idx]['y'] = y.tolist()

    def _handle_relayout(self, event: GenericEventArguments) -> None:
        """Handle plotly_relayout event for zoom/pan."""
        args = event.args

        x_range = self._extract_x_range(args)
        if x_range is None:
            if 'xaxis.autorange' in args or 'autosize' in args:
                self._apply_resampling(x_range=None)
                self.update()
            return

        self._apply_resampling(x_range=x_range)
        self.update()

    def _extract_x_range(self, relayout_data: dict) -> tuple[float, float] | None:
        """Extract the primary x-axis range from relayout event data.

        Handles both the split ``xaxis.range[0]``/``xaxis.range[1]`` keys and the combined
        ``xaxis.range`` list. Only the primary x-axis is tracked; subplot axes are ignored.
        """
        x0, x1 = None, None
        for key, value in relayout_data.items():
            if key == 'xaxis.range' and isinstance(value, (list, tuple)) and len(value) == 2:
                x0, x1 = value[0], value[1]
            elif key == 'xaxis.range[0]':
                x0 = value
            elif key == 'xaxis.range[1]':
                x1 = value
        if x0 is None or x1 is None:
            return None
        numeric = to_numeric(np.asarray([x0, x1]))  # ranges may arrive as datetime strings on a time axis
        if numeric is None:
            return None
        return (float(numeric[0]), float(numeric[1]))

    def update_figure(self, figure: dict | go.Figure):
        """Overrides figure instance of this Plotly chart and updates chart on client side."""
        if self._downsampler:
            figure = copy.deepcopy(figure)  # resampling rewrites trace data, so never mutate the caller's figure
        self.figure = figure
        if self._downsampler:
            self._hf_data.clear()
            self._extract_hf_data()
            self._apply_resampling()
        self.update()

    def run_plot_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """Run a plotly.js library function against the chart's HTML element.

        See the `plotly.js function reference <https://plotly.com/javascript/plotlyjs-function-reference/>`_ for a list of methods.
        The chart's HTML element is passed as the first argument automatically.

        If the function is awaited, the result of the method call is returned
        (unless it resolves to the chart's HTML element, in which case ``None`` is returned).
        Otherwise, the method is executed without waiting for a response.

        *Added in version 3.13.0*

        :param name: name of the plotly.js function (without the ``Plotly.`` prefix)
        :param args: arguments to pass after the chart element
        :param timeout: timeout in seconds (default: 1 second)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('run_plot_method', name, *args, timeout=timeout)

    def update(self) -> None:
        with self._props.suspend_updates():
            self._props['options'] = self._get_figure_json()
        super().update()

    def _get_figure_json(self) -> dict:
        if optional_features.has('plotly') and isinstance(self.figure, go.Figure):
            # convert go.Figure to dict object which is directly JSON serializable
            # orjson supports NumPy array serialization
            return self.figure.to_plotly_json()

        if isinstance(self.figure, dict):
            # already a dict object with keys: data, layout, config (optional)
            return self.figure

        raise ValueError(f'Plotly figure is of unknown type "{self.figure.__class__.__name__}".')
