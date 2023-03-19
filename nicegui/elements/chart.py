from typing import Dict, List

from ..dependencies import js_dependencies, register_component
from ..element import Element

dependencies = [
    'lib/highcharts/highcharts.js',
    'lib/highcharts/highcharts-more.js',
    'lib/highcharts/highcharts-3d.js',
]
optional_dependencies = [
    'lib/highcharts/modules/sankey.js',
    'lib/highcharts/modules/accessibility.js',
    'lib/highcharts/modules/exporting.js',
    'lib/highcharts/modules/export-data.js',
    'lib/highcharts/modules/solid-gauge.js',
    'lib/highcharts/modules/annotations-advanced.js',
    'lib/highcharts/modules/annotations.js',
    'lib/highcharts/modules/arc-diagram.js',
    'lib/highcharts/modules/arrow-symbols.js',
    'lib/highcharts/modules/boost-canvas.js',
    'lib/highcharts/modules/boost.js',
    'lib/highcharts/modules/broken-axis.js',
    'lib/highcharts/modules/bullet.js',
    'lib/highcharts/modules/coloraxis.js',
    'lib/highcharts/modules/current-date-indicator.js',
    'lib/highcharts/modules/datagrouping.js',
    'lib/highcharts/modules/data.js',
    'lib/highcharts/modules/debugger.js',
    'lib/highcharts/modules/dependency-wheel.js',
    'lib/highcharts/modules/dotplot.js',
    'lib/highcharts/modules/draggable-points.js',
    'lib/highcharts/modules/drag-panes.js',
    'lib/highcharts/modules/drilldown.js',
    'lib/highcharts/modules/dumbbell.js',
    'lib/highcharts/modules/full-screen.js',
    'lib/highcharts/modules/funnel.js',
    'lib/highcharts/modules/gantt.js',
    'lib/highcharts/modules/grid-axis.js',
    'lib/highcharts/modules/heatmap.js',
    'lib/highcharts/modules/histogram-bellcurve.js',
    'lib/highcharts/modules/item-series.js',
    'lib/highcharts/modules/lollipop.js',
    'lib/highcharts/modules/marker-clusters.js',
    'lib/highcharts/modules/networkgraph.js',
    'lib/highcharts/modules/no-data-to-display.js',
    'lib/highcharts/modules/offline-exporting.js',
    'lib/highcharts/modules/oldie.js',
    'lib/highcharts/modules/oldie-polyfills.js',
    'lib/highcharts/modules/organization.js',
    'lib/highcharts/modules/overlapping-datalabels.js',
    'lib/highcharts/modules/parallel-coordinates.js',
    'lib/highcharts/modules/pareto.js',
    'lib/highcharts/modules/pathfinder.js',
    'lib/highcharts/modules/pattern-fill.js',
    'lib/highcharts/modules/price-indicator.js',
    'lib/highcharts/modules/series-label.js',
    'lib/highcharts/modules/series-on-point.js',
    'lib/highcharts/modules/sonification.js',
    'lib/highcharts/modules/static-scale.js',
    'lib/highcharts/modules/stock.js',
    'lib/highcharts/modules/stock-tools.js',
    'lib/highcharts/modules/streamgraph.js',
    'lib/highcharts/modules/sunburst.js',
    'lib/highcharts/modules/tilemap.js',
    'lib/highcharts/modules/timeline.js',
    'lib/highcharts/modules/treegraph.js',
    'lib/highcharts/modules/treegrid.js',
    'lib/highcharts/modules/variable-pie.js',
    'lib/highcharts/modules/variwide.js',
    'lib/highcharts/modules/vector.js',
    'lib/highcharts/modules/venn.js',
    'lib/highcharts/modules/windbarb.js',
    'lib/highcharts/modules/wordcloud.js',
    'lib/highcharts/modules/xrange.js',
    'lib/highcharts/modules/funnel3d.js',
    'lib/highcharts/modules/heikinashi.js',
    'lib/highcharts/modules/hollowcandlestick.js',
    'lib/highcharts/modules/pyramid3d.js',
    'lib/highcharts/modules/cylinder.js',
]
register_component('chart', __file__, 'chart.js', dependencies, optional_dependencies)


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
        self._props['extras'] = [
            dependency.import_path
            for dependency in js_dependencies.values()
            if dependency.optional and dependency.path.stem in extras and 'chart' in dependency.dependents
        ]

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
