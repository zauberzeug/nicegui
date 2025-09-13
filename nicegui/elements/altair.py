from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING, Any

from .. import optional_features
from ..elements.anywidget import AnyWidget

if importlib.util.find_spec('altair'):
    optional_features.register('altair')
    if TYPE_CHECKING:
        import altair


class Altair(AnyWidget):
    def __init__(self, chart: altair.Chart | altair.JupyterChart, **kwargs: Any) -> None:
        """Wrap an altair chart in NiceGUI via anywidget

        Refer to `AnyWidget` for more details.
        """
        import altair
        if isinstance(chart, altair.Chart):
            chart = altair.JupyterChart(chart)
        super().__init__(chart, **kwargs)
