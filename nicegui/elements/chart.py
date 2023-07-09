from pathlib import Path
from typing import Dict, List

from ..element import Element

base = Path(__file__).parent
libraries = [p.relative_to(base) for p in sorted((base / 'lib' / 'highcharts').glob('*.js'), key=lambda p: p.stem)]
modules = {p.stem: p.relative_to(base) for p in sorted((base / 'lib' / 'highcharts' / 'modules').glob('*.js'))}


class Chart(Element, component='chart.js', libraries=libraries, extra_libraries=list(modules.values())):

    def __init__(self, options: Dict, *, type: str = 'chart', extras: List[str] = []) -> None:
        """Chart

        An element to create a chart using `Highcharts <https://www.highcharts.com/>`_.
        Updates can be pushed to the chart by changing the `options` property.
        After data has changed, call the `update` method to refresh the chart.

        By default, a `Highcharts.chart` is created.
        To use, e.g., `Highcharts.stockChart` instead, set the `type` property to "stockChart".

        :param options: dictionary of Highcharts options
        :param type: chart type (e.g. "chart", "stockChart", "mapChart", ...; default: "chart")
        :param extras: list of extra dependencies to include (e.g. "annotations", "arc-diagram", "solid-gauge", ...)
        """
        super().__init__()
        self._props['type'] = type
        self._props['options'] = options
        self._props['extras'] = extras
        self.libraries.extend(library for library in self.extra_libraries if library.path.stem in extras)

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
