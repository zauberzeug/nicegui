from pathlib import Path
from typing import Dict, Union

import plotly.graph_objects as go

from ..dependencies import register_library, register_vue_component
from ..element import Element

register_vue_component(name='plotly', path=Path(__file__).parent.joinpath('plotly.vue'))
register_library(name='plotly', path=Path(__file__).parent.joinpath('lib', 'plotly', 'plotly.min.js'))


class Plotly(Element):

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
        super().__init__('plotly')
        self.use_library('plotly')

        self.figure = figure
        self.update()

    def update_figure(self, figure: Union[Dict, go.Figure]):
        """Overrides figure instance of this Plotly chart and updates chart on client side."""
        self.figure = figure
        self.update()

    def update(self) -> None:
        options = self._get_figure_json()
        options['config'] = \
            {**options['config'], **{'responsive': True}} if 'config' in options else {'responsive': True}
        self._props['options'] = options
        self.run_method('update', self._props['options'])

    def _get_figure_json(self) -> Dict:
        if isinstance(self.figure, go.Figure):
            # convert go.Figure to dict object which is directly JSON serializable
            # orjson supports numpy array serialization
            return self.figure.to_plotly_json()

        if isinstance(self.figure, dict):
            # already a dict object with keys: data, layout, config (optional)
            return self.figure

        raise ValueError(f'Plotly figure is of unknown type "{self.figure.__class__.__name__}".')
