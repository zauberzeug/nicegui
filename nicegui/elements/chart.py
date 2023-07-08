from pathlib import Path
from typing import Dict, List

from ..dependencies import Library, register_library, register_vue_component
from ..element import Element

component = register_vue_component(Path('chart.js'))

core_dependencies: List[Library] = []
extra_dependencies: Dict[str, Library] = {}
base = Path(__file__).parent / 'lib'
for path in sorted((base / 'highcharts').glob('*.js'), key=lambda p: p.stem):
    core_dependencies.append(register_library(path.relative_to(base)))
for path in sorted((base / 'highcharts' / 'modules').glob('*.js'), key=lambda p: p.stem):
    extra_dependencies[path.stem] = register_library(path.relative_to(base))


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
        super().__init__(component.tag)
        self._props['type'] = type
        self._props['options'] = options
        self._props['extras'] = extras
        self.use_component(component)
        for dependency in core_dependencies:
            self.use_library(dependency)
        for extra in extras:
            self.use_library(extra_dependencies[extra])

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
