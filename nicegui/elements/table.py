import asyncio
from typing import Dict

import justpy as jp

from .. import globals
from ..task_logger import create_task
from .element import Element

jp.template_options['aggrid'] = False


class Table(Element):

    def __init__(self, options: Dict):
        """Table

        An element to create a table using `AG Grid <https://www.ag-grid.com/>`_.

        :param options: dictionary of AG Grid options
        """
        view = jp.AgGrid(temp=False)
        view.options = self.options = jp.Dict(**options)
        super().__init__(view)

        if not jp.template_options['aggrid'] and globals.loop and globals.loop.is_running():
            create_task(self.page.run_javascript('location.reload()'))
        jp.template_options['aggrid'] = True
