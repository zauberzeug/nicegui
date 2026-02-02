from __future__ import annotations

import re

import numpy as np

from ... import optional_features
from ...element import Element
from ...events import GenericEventArguments
from ._resampling import HFTraceData, create_downsampler

try:
    import plotly.graph_objects as go
    optional_features.register('plotly')
except ImportError:
    pass


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
                          For better performance, install ``pip install nicegui[tsdownsample]``.
        """
        super().__init__()

        self.figure = figure
        self._n_samples = n_samples
        self._hf_data: dict[str, HFTraceData] = {}

        if n_samples:
            self._downsampler = create_downsampler()
            self._extract_hf_data()
            self._apply_resampling()
            self.on('plotly_relayout', self._handle_relayout)
        else:
            self._downsampler = None

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
                continue

            x = trace_dict.get('x')
            y = trace_dict.get('y')
            if x is None or y is None:
                continue

            x_arr = np.asarray(x, dtype=np.float64)
            y_arr = np.asarray(y, dtype=np.float64)

            # Remove NaN values (tsdownsample requires no NaNs in x-data and handles y-data poorly)
            valid_mask = ~(np.isnan(x_arr) | np.isnan(y_arr))
            x_arr = x_arr[valid_mask]
            y_arr = y_arr[valid_mask]

            if len(x_arr) < (self._n_samples or 0):
                continue

            # tsdownsample requires x-data to be monotonically increasing (sorted)
            if not np.all(x_arr[:-1] <= x_arr[1:]):
                sort_indices = np.argsort(x_arr)
                x_arr = x_arr[sort_indices]
                y_arr = y_arr[sort_indices]

            uid = trace_dict.get('uid') or f'trace_{idx}'
            self._hf_data[uid] = HFTraceData(x=x_arr,y=y_arr,trace_idx=idx)

    def _apply_resampling(self, x_range: tuple[float, float] | None = None) -> None:
        """Apply resampling to all stored high-frequency traces."""
        if not self._downsampler or not self._n_samples:
            return

        for _, hf in self._hf_data.items():
            x_arr = hf.x
            y_arr = hf.y

            if x_range is not None:
                mask = (x_arr >= x_range[0]) & (x_arr <= x_range[1])
                indices_in_range = np.where(mask)[0]
                if len(indices_in_range) == 0:
                    continue
                start_idx, end_idx = indices_in_range[0], indices_in_range[-1] + 1
            else:
                start_idx, end_idx = 0, len(x_arr)

            slice_len = end_idx - start_idx
            n_out = min(self._n_samples, slice_len)

            if slice_len <= n_out:
                sampled_x = x_arr[start_idx:end_idx]
                sampled_y = y_arr[start_idx:end_idx]
            else:
                x_slice = x_arr[start_idx:end_idx]
                y_slice = y_arr[start_idx:end_idx]

                x_numeric = x_slice.astype(np.float64) if not np.issubdtype(x_slice.dtype, np.number) else x_slice
                y_numeric = y_slice.astype(np.float64) if not np.issubdtype(y_slice.dtype, np.number) else y_slice

                indices = self._downsampler.downsample(x_numeric, y_numeric, n_out=n_out)
                sampled_x = x_slice[indices]
                sampled_y = y_slice[indices]

            self._update_trace_data(hf.trace_idx, sampled_x, sampled_y)

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
        """Extract x-axis range from relayout event data."""
        x0, x1 = None, None
        for key, value in relayout_data.items():
            if match := re.match(r'^xaxis\d*\.range\[([01])\]$', key):
                if match.group(1) == '0':
                    x0 = value
                else:
                    x1 = value
        if x0 is not None and x1 is not None:
            return (float(x0), float(x1))
        return None

    def update_figure(self, figure: dict | go.Figure):
        """Overrides figure instance of this Plotly chart and updates chart on client side."""
        self.figure = figure
        if self._downsampler:
            self._hf_data.clear()
            self._extract_hf_data()
            self._apply_resampling()
        self.update()

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
