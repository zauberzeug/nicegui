from typing import Dict

from ..element import Element


class ECharts(Element, component='echarts.js', libraries=['lib/echarts/echarts.min.js']):

    def __init__(self, options: Dict) -> None:
        """Apache ECharts

        An element to create a chart using `ECharts <https://echarts.apache.org/>`_.
        Updates can be pushed to the chart by changing the `options` property.
        After data has changed, call the `update` method to refresh the chart.

        :param options: dictionary of EChart options
        """
        super().__init__()
        self._props['options'] = options
        self._classes = ['nicegui-echarts']

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
