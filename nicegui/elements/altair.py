from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING

from .. import optional_features
from .anywidget import AnyWidget

if importlib.util.find_spec('altair'):
    optional_features.register('altair')
    if TYPE_CHECKING:
        import altair


class Altair(AnyWidget):

    def __init__(self, chart: altair.TopLevelSpec | altair.JupyterChart, *, throttle: float = 0) -> None:
        """Altair Chart

        Wrap an Altair chart in NiceGUI via anywidget.

        Refer to the `altair documentation <https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html#accessing-variable-params>`_
        for more information about synchronizing Altair parameters with Python.

        *Added in version 3.5.0*

        :param chart: the chart to wrap
        :param throttle: minimum time (in seconds) between widget updates to Python (default: 0.0)
        """
        import altair  # pylint: disable=import-outside-toplevel

        if isinstance(chart, altair.TopLevelSpec):
            chart = altair.JupyterChart(chart)

        super().__init__(chart, throttle=throttle)  # type: ignore[arg-type]
