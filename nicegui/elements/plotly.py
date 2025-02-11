from __future__ import annotations

from typing import Dict, Union

from .. import optional_features
from ..element import Element

try:
    import plotly.graph_objects as go
    optional_features.register('plotly')
except ImportError:
    pass


class Plotly(Element, component='plotly.vue', dependencies=['lib/plotly/plotly.min.js']):

    def __init__(self, figure: Union[Dict, go.Figure]) -> None:
        """Plotly Element

        Renders a Plotly chart.
        There are two ways to pass a Plotly figure for rendering, see parameter `figure`:

        * Pass a `go.Figure` object, see https://plotly.com/python/

        * Pass a Python `dict` object with keys `data`, `layout`, `config` (optional), see https://plotly.com/javascript/

        For best performance, use the declarative `dict` approach for creating a Plotly chart.

        :param figure: Plotly figure to be rendered. Can be either a `go.Figure` instance, or
                       a `dict` object with keys `data`, `layout`, `config` (optional).
        """
        if not optional_features.has('plotly'):
            raise ImportError('Plotly is not installed. Please run "pip install nicegui[plotly]".')

        super().__init__()

        self.figure = figure
        self.update()
        self._classes.append('js-plotly-plot')

    def update_figure(self, figure: Union[Dict, go.Figure]):
        """Overrides figure instance of this Plotly chart and updates chart on client side."""
        self.figure = figure
        self.update()

    def update(self) -> None:
        self._props['options'] = self._get_figure_json()
        super().update()
        self.run_method('update')

    def _get_figure_json(self) -> Dict:
        if isinstance(self.figure, go.Figure):
            # convert go.Figure to dict object which is directly JSON serializable
            # orjson supports NumPy array serialization
            return self.figure.to_plotly_json()

        if isinstance(self.figure, dict):
            # already a dict object with keys: data, layout, config (optional)
            return self.figure

        raise ValueError(f'Plotly figure is of unknown type "{self.figure.__class__.__name__}".')
