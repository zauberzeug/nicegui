from typing import Literal, Optional

from ..dependencies import register_component
from ..element import Element
from ..functions.javascript import run_javascript

register_component('q_table', __file__, 'qtable.js')


class QTable(Element):
    def __init__(
        self,
        columns: Optional[dict] = [],
        rows: Optional[list] = [],
        title: Optional[str] = None,
        selection_mode: Optional[Literal['single', 'multiple', 'none']] = 'none',
        selection_key: Optional[str] = '',
        filter_config: Optional[dict] = {
            'label': 'Search...',
            'icon': 'search',
            'color': 'primary',
            'dense': True,
        },
    ):
        """QTable
        """

        super().__init__('q_table')

        self._props['columns'] = columns
        self._props['rows'] = rows

        self._props['title'] = title

        self._props['selection_mode'] = selection_mode
        self._props['selection_key'] = selection_key

        self._props['filter_config'] = filter_config

        self.selected = []
        self.on('selected', handler=self.handle_selected_event)

    def set_data(self, data):
        self._props['rows'] = data

        self.update()
        self.run_method('evalFunction')

    def handle_selected_event(self, data):
        self.selected = data['args']

    async def __dump__(self):
        await run_javascript(f'console.info(getElement({self.id}))', respond=False)
