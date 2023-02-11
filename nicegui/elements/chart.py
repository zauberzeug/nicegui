from typing import Dict, List

from ..dependencies import js_dependencies, register_component
from ..element import Element

dependencies = [
    'lib/highcharts.js',
    'lib/highcharts-more.js',
    'lib/highcharts-3d.js',
]
optional_dependencies = [
    'lib/highcharts_modules/sankey.js',
    'lib/highcharts_modules/accessibility.js',
    'lib/highcharts_modules/exporting.js',
    'lib/highcharts_modules/export-data.js',
    'lib/highcharts_modules/solid-gauge.js',
    'lib/highcharts_modules/annotations-advanced.js',
    'lib/highcharts_modules/annotations.js',
    'lib/highcharts_modules/arc-diagram.js',
    'lib/highcharts_modules/arrow-symbols.js',
    'lib/highcharts_modules/boost-canvas.js',
    'lib/highcharts_modules/boost.js',
    'lib/highcharts_modules/broken-axis.js',
    'lib/highcharts_modules/bullet.js',
    'lib/highcharts_modules/coloraxis.js',
    'lib/highcharts_modules/current-date-indicator.js',
    'lib/highcharts_modules/datagrouping.js',
    'lib/highcharts_modules/data.js',
    'lib/highcharts_modules/debugger.js',
    'lib/highcharts_modules/dependency-wheel.js',
    'lib/highcharts_modules/dotplot.js',
    'lib/highcharts_modules/draggable-points.js',
    'lib/highcharts_modules/drag-panes.js',
    'lib/highcharts_modules/drilldown.js',
    'lib/highcharts_modules/dumbbell.js',
    'lib/highcharts_modules/full-screen.js',
    'lib/highcharts_modules/funnel.js',
    'lib/highcharts_modules/gantt.js',
    'lib/highcharts_modules/grid-axis.js',
    'lib/highcharts_modules/heatmap.js',
    'lib/highcharts_modules/histogram-bellcurve.js',
    'lib/highcharts_modules/item-series.js',
    'lib/highcharts_modules/lollipop.js',
    'lib/highcharts_modules/marker-clusters.js',
    'lib/highcharts_modules/networkgraph.js',
    'lib/highcharts_modules/no-data-to-display.js',
    'lib/highcharts_modules/offline-exporting.js',
    'lib/highcharts_modules/oldie.js',
    'lib/highcharts_modules/oldie-polyfills.js',
    'lib/highcharts_modules/organization.js',
    'lib/highcharts_modules/overlapping-datalabels.js',
    'lib/highcharts_modules/parallel-coordinates.js',
    'lib/highcharts_modules/pareto.js',
    'lib/highcharts_modules/pathfinder.js',
    'lib/highcharts_modules/pattern-fill.js',
    'lib/highcharts_modules/price-indicator.js',
    'lib/highcharts_modules/series-label.js',
    'lib/highcharts_modules/series-on-point.js',
    'lib/highcharts_modules/sonification.js',
    'lib/highcharts_modules/static-scale.js',
    'lib/highcharts_modules/stock.js',
    'lib/highcharts_modules/stock-tools.js',
    'lib/highcharts_modules/streamgraph.js',
    'lib/highcharts_modules/sunburst.js',
    'lib/highcharts_modules/tilemap.js',
    'lib/highcharts_modules/timeline.js',
    'lib/highcharts_modules/treegraph.js',
    'lib/highcharts_modules/treegrid.js',
    'lib/highcharts_modules/variable-pie.js',
    'lib/highcharts_modules/variwide.js',
    'lib/highcharts_modules/vector.js',
    'lib/highcharts_modules/venn.js',
    'lib/highcharts_modules/windbarb.js',
    'lib/highcharts_modules/wordcloud.js',
    'lib/highcharts_modules/xrange.js',
    'lib/highcharts_modules/funnel3d.js',
    'lib/highcharts_modules/heikinashi.js',
    'lib/highcharts_modules/hollowcandlestick.js',
    'lib/highcharts_modules/pyramid3d.js',
    'lib/highcharts_modules/cylinder.js',
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
