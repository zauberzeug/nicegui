from typing import Optional

from typing_extensions import Literal

from ..dependencies import register_component
from ..element import Element

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
        """Quasar Table

        A component that allows you to display data in a tabular manner.

        :param columns: A list of column objects.
        :param rows: A list of row objects.
        :param title: The title of the table.
        :param selection_mode: defines the selection behavior.
            'single': only one cell can be selected at a time.
            'multiple': more than one cell can be selected at a time.
            'none': no cells can be selected.
        :param selection_key: A unique key used to identify a row.
        :param filter_config: A dict of config options for filter/search text-input.

        API to get the selected data in the table:
        :property selected: A list of selected rows.
            Each row is represented by a dict.
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
