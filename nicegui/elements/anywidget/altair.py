from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING, Any

from ... import optional_features
from .anywidget import AnyWidget

if importlib.util.find_spec('altair'):
    optional_features.register('altair')
    if TYPE_CHECKING:
        import altair


class Altair(AnyWidget):
    def __init__(self, chart: altair.Chart | altair.JupyterChart, **kwargs: Any) -> None:
        """altair Chart

        Wrap an `altair.Chart` or `altair.JupyterChart` in NiceGUI via `anywidget`.

        Refer to the `altair documentation <https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html#accessing-variable-params>`_
        for more information about synchronizing `altair` parameters with python.

        :param chart: the `altair.Chart` or `altair.JupyterChart` to wrap
        :param throttle: minimum time (in seconds) between widget updates to python (default: 0.0)
        """
        import altair
        if isinstance(chart, altair.Chart):
            chart = altair.JupyterChart(chart)
        super().__init__(chart, **kwargs)
