from typing import Dict

import justpy as jp

from .element import Element


class Table(Element):

    def __init__(self, options: Dict):
        """Table

        An element to create a table using `AG Grid <https://www.ag-grid.com/>`_.

        :param options: dictionary of AG Grid options
        """
        view = jp.AgGrid(temp=False)
        view.options = self.options = jp.Dict(**options)
        super().__init__(view)
