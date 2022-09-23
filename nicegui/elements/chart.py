from typing import Dict

import justpy as jp

from .element import Element


class Chart(Element):

    def __init__(self, options: Dict):
        """Chart

        An element to create a chart using `Highcharts <https://www.highcharts.com/>`_.

        :param options: dictionary of Highcharts options
        """
        view = jp.HighCharts(temp=False)
        view.options = self.options = jp.Dict(**options)
        super().__init__(view)
