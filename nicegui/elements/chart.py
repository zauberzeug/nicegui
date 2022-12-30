from typing import Dict, List

from ..element import Element
from ..vue import js_extra_dependencies, register_component

register_component('chart', __file__, 'chart.js',
                   ['lib/highcharts.js',
                    'lib/highcharts-more.js',
                    'lib/highcharts-3d.js',
                    ],
                   ['modules/sankey.js',
                    'modules/accessibility.js',
                    'modules/exporting.js',
                    'modules/export-data.js',
                    'modules/solid-gauge.js',
                    'modules/annotations-advanced.js',
                    'modules/annotations.js',
                    'modules/arc-diagram.js',
                    'modules/arrow-symbols.js',
                    'modules/boost-canvas.js',
                    'modules/boost.js',
                    'modules/broken-axis.js',
                    'modules/bullet.js',
                    'modules/coloraxis.js',
                    'modules/current-date-indicator.js',
                    'modules/datagrouping.js',
                    'modules/data.js',
                    'modules/debugger.js',
                    'modules/dependency-wheel.js',
                    'modules/dotplot.js',
                    'modules/draggable-points.js',
                    'modules/drag-panes.js',
                    'modules/drilldown.js',
                    'modules/dumbbell.js',
                    'modules/full-screen.js',
                    'modules/funnel.js',
                    'modules/gantt.js',
                    'modules/grid-axis.js',
                    'modules/heatmap.js',
                    'modules/histogram-bellcurve.js',
                    'modules/item-series.js',
                    'modules/lollipop.js',
                    'modules/marker-clusters.js',
                    'modules/networkgraph.js',
                    'modules/no-data-to-display.js',
                    'modules/offline-exporting.js',
                    'modules/oldie.js',
                    'modules/oldie-polyfills.js',
                    'modules/organization.js',
                    'modules/overlapping-datalabels.js',
                    'modules/parallel-coordinates.js',
                    'modules/pareto.js',
                    'modules/pathfinder.js',
                    'modules/pattern-fill.js',
                    'modules/price-indicator.js',
                    'modules/series-label.js',
                    'modules/series-on-point.js',
                    'modules/sonification.js',
                    'modules/static-scale.js',
                    'modules/stock.js',
                    'modules/stock-tools.js',
                    'modules/streamgraph.js',
                    'modules/sunburst.js',
                    'modules/tilemap.js',
                    'modules/timeline.js',
                    'modules/treegraph.js',
                    'modules/treegrid.js',
                    'modules/variable-pie.js',
                    'modules/variwide.js',
                    'modules/vector.js',
                    'modules/venn.js',
                    'modules/windbarb.js',
                    'modules/wordcloud.js',
                    'modules/xrange.js',
                    'modules/funnel3d.js',
                    'modules/heikinashi.js',
                    'modules/hollowcandlestick.js',
                    'modules/pyramid3d.js',
                    'modules/cylinder.js',
                    ])


class Chart(Element):

    def __init__(self, options: Dict, *, extras: List[str] = []) -> None:
        """Chart

        An element to create a chart using `Highcharts <https://www.highcharts.com/>`_.
        Updates can be pushed to the chart by changing the `options` property.
        After data has changed, call the `update` method to refresh the chart.

        :param options: dictionary of Highcharts options
        :param extras: list of extra dependencies to include (e.g. "annotations", "arc-diagram", "solid-gauge", ...)
        """
        super().__init__('chart')
        self._props['options'] = options
        urls = [f'/_nicegui/dependencies/{id}/{dependency.path.name}'
                for id, dependency in js_extra_dependencies.items()
                if dependency.path.stem in extras and 'chart' in dependency.dependents]
        self._props['extras'] = urls

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
