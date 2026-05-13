from __future__ import annotations

from contextlib import suppress

from ... import optional_features
from ...element import Element

with suppress(ImportError):
    import plotly.graph_objects as go
    optional_features.register('plotly')


class Plotly(Element, component='plotly.js', esm={'nicegui-plotly': 'dist'}):

    def __init__(self, figure: dict | go.Figure) -> None:
        """Plotly Element

        Renders a Plotly chart.
        There are two ways to pass a Plotly figure for rendering, see parameter `figure`:

        * Pass a `go.Figure` object, see https://plotly.com/python/

        * Pass a Python `dict` object with keys `data`, `layout`, `config` (optional), see https://plotly.com/javascript/

        For best performance, use the declarative `dict` approach for creating a Plotly chart.

        :param figure: Plotly figure to be rendered. Can be either a `go.Figure` instance, or
                       a `dict` object with keys `data`, `layout`, `config` (optional).
        """
        super().__init__()

        self.figure = figure
        self.update()
        self._classes.append('js-plotly-plot')
        self._update_method = 'update'

    def update_figure(self, figure: dict | go.Figure):
        """Overrides figure instance of this Plotly chart and updates chart on client side."""
        self.figure = figure
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
