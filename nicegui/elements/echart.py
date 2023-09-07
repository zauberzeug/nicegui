from typing import Callable, Dict, Optional

from ..element import Element
from ..events import (EChartPointClickEventArguments, GenericEventArguments, handle_event)


class EChart(Element, component='echart.js', libraries=['lib/echarts/echarts.min.js']):

    def __init__(self, options: Dict,
            on_point_click: Optional[Callable] = None,
            ) -> None:
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
                    event_type='point_click',
                    component_type=e.args['component_type'],
                    series_type=e.args['series_type'],
                    series_index=e.args['series_index'],
                    series_name=e.args['series_name'],
                    name=e.args['name'],
                    data_index=e.args['data_index'],
                    data=e.args['data'],
                    data_type=e.args.get('data_type'),
                    value=e.args['value'],
                ))
            
            self.on('pointClick', handle_point_click, [
                'component_type', 
                'series_type',
                'series_index', 
                'series_name',
                'name',
                'data_index', 
                'data',
                'data_type',
                'value',
                ])

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
