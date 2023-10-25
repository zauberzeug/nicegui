from typing import Callable, Dict, Optional

from ..element import Element
from ..events import EChartPointClickEventArguments, GenericEventArguments, handle_event


class EChart(Element, component='echart.js', libraries=['lib/echarts/echarts.min.js']):

    def __init__(self, options: Dict, on_point_click: Optional[Callable] = None) -> None:
        """Apache EChart

        An element to create a chart using `ECharts <https://echarts.apache.org/>`_.
        Updates can be pushed to the chart by changing the `options` property.
        After data has changed, call the `update` method to refresh the chart.

        :param options: dictionary of EChart options
        :param on_click_point: callback function that is called when a point is clicked
        """
        super().__init__()
        self._props['options'] = options
        self._classes = ['nicegui-echart']

        if on_point_click:
            def handle_point_click(e: GenericEventArguments) -> None:
                handle_event(on_point_click, EChartPointClickEventArguments(
                    sender=self,
                    client=self.client,
                    component_type=e.args['componentType'],
                    series_type=e.args['seriesType'],
                    series_index=e.args['seriesIndex'],
                    series_name=e.args['seriesName'],
                    name=e.args['name'],
                    data_index=e.args['dataIndex'],
                    data=e.args['data'],
                    data_type=e.args.get('dataType'),
                    value=e.args['value'],
                ))
            self.on('pointClick', handle_point_click, [
                'componentType',
                'seriesType',
                'seriesIndex',
                'seriesName',
                'name',
                'dataIndex',
                'data',
                'dataType',
                'value',
            ])

    @property
    def options(self) -> Dict:
        """The options dictionary."""
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
