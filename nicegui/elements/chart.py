import asyncio
from typing import Dict

import justpy as jp

from ..task_logger import create_task
from .element import Element

jp.template_options['highcharts'] = False


class Chart(Element):

    def __init__(self, options: Dict):
        """Chart

        An element to create a chart using `Highcharts <https://www.highcharts.com/>`_.

        :param options: dictionary of Highcharts options
        """
        view = jp.HighCharts(temp=False)
        view.options = self.options = jp.Dict(**options)
        super().__init__(view)

        if not jp.template_options['highcharts'] and asyncio.get_event_loop().is_running():
            create_task(self.page.run_javascript('location.reload()'))
        jp.template_options['highcharts'] = True
