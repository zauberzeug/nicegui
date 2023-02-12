import json

import plotly.graph_objects as go

from ..dependencies import js_dependencies, register_component
from ..element import Element

register_component('plotly', __file__, 'plotly.js', [], ['lib/plotly.min.js'])


class Plotly(Element):

    def __init__(self, figure: go.Figure) -> None:
        """Plotly Element

        Renders a plotly figure onto the page.

        See `plotly documentation <https://plotly.com/python/>`_ for more information.

        :param figure: the plotly figure to be displayed
        """
        super().__init__('plotly')
        self.figure = figure
        self._props['lib'] = [d.import_path for d in js_dependencies.values() if d.path.name == 'plotly.min.js'][0]
        self.update()

    def update(self) -> None:
        self._props['options'] = json.loads(self.figure.to_json())
        self.run_method('update', self._props['options'])
