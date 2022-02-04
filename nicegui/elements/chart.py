import justpy as jp

from .element import Element


class Chart(Element):
    def __init__(self, options):
        """Chart

        An element to create a chart (`<https://www.highcharts.com/>`_).

        :param options: dictionary of highchart options
        """
        view = jp.HighCharts(classes='m-2 p-2 border', style='width: 600px')
        view.options = self.options = jp.Dict(**options)
        super().__init__(view)
