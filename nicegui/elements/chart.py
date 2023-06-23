from pathlib import Path
from typing import Dict, List

from ..dependencies import register_library, register_vue_component
from ..element import Element

register_vue_component('chart', Path(__file__).parent / 'chart.js')

core_dependencies: List[Path] = []
for path in sorted((Path(__file__).parent / 'lib' / 'highcharts').glob('*.js'), key=lambda p: p.stem):
    register_library(path.stem, path)
    core_dependencies.append(path)
for path in sorted((Path(__file__).parent / 'lib' / 'highcharts' / 'modules').glob('*.js'), key=lambda p: p.stem):
    register_library(path.stem, path)


class Chart(Element):

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
        super().__init__('chart')
        self._props['type'] = type
        self._props['options'] = options
        self._props['extras'] = extras
        self.use_component('chart')
        for dependency in core_dependencies:
            self.use_library(dependency.stem)
        for extra in extras:
            self.use_library(extra)

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
