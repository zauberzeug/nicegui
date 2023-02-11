from typing import Dict, List

from ..dependencies import register_component
from ..element import Element

register_component('table', __file__, 'table.js', ['lib/ag-grid-community.min.js'])


class Table(Element):

    def __init__(self, options: Dict, *, html_columns: List[int] = [], theme: str = 'balham') -> None:
        """Table

        An element to create a table using `AG Grid <https://www.ag-grid.com/>`_.

        :param options: dictionary of AG Grid options
        :param html_columns: list of columns that should be rendered as HTML (default: `[]`)
        :param theme: AG Grid theme (default: 'balham')
        """
        super().__init__('table')
        self._props['options'] = options
        self._props['html_columns'] = html_columns
        self._classes = [f'ag-theme-{theme}', 'w-full', 'h-64']

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_grid')

    def call_api_method(self, name: str, *args) -> None:
        self.run_method('call_api_method', name, *args)
