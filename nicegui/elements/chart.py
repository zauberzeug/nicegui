import justpy as jp

from .element import Element
from typing import Dict


class Chart(Element):
    def __init__(self, options):
        """Highcharts Element

        An element to create highchart tables.

        :param options: dictionary of highchart options
        """
        view = jp.HighCharts(classes='m-2 p-2 border', style='width: 600px')
        self.options = jp.Dict(**options)
        view.options = self.options
        super().__init__(view)
