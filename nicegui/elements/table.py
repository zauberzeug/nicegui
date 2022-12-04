from typing import Dict

from .. import vue
from ..element import Element

vue.register_component('table', __file__, 'table.js', ['lib/ag-grid-community.min.js'])


class Table(Element):

    def __init__(self, options: Dict, *, theme: str = 'balham') -> None:
        """Table

        An element to create a table using `AG Grid <https://www.ag-grid.com/>`_.

        :param options: dictionary of AG Grid options
        :param theme: AG Grid theme (default: 'balham')
        """
        super().__init__('table')
        self._props['options'] = options
        self._classes = [f'ag-theme-{theme}', 'w-full', 'h-64']

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_grid')

    def call_api_method(self, name: str, *args) -> None:
        self.run_method('call_api_method', name, args)
