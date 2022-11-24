from typing import Dict

from ..element import Element
from ..vue import register_component

register_component('chart', __file__, 'chart.js', ['lib/highcharts.js'])


class Chart(Element):

    def __init__(self, options: Dict) -> None:
        """Chart

        An element to create a chart using `Highcharts <https://www.highcharts.com/>`_.
        Updates can be pushed to the chart by changing the `options` property.
        After data has changed, call the `update` method to refresh the chart.

        :param options: dictionary of Highcharts options
        """
        super().__init__('chart')
        self._props['options'] = options

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
