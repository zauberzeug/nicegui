from typing import Callable, Optional

from typing_extensions import Literal

from .mixins.value_element import ValueElement
from ..element import Element


class QTr(Element):
    def __init__(self) -> None:
        super().__init__('q-tr')


class QTh(Element):
    def __init__(self) -> None:
        super().__init__('q-th')


class QTd(Element):
    def __init__(self, key: str = '') -> None:
        super().__init__('q-td')
        if key:
            self._props['key'] = key


class QTable(ValueElement):
    VALUE_PROP = 'filter'

    # Scope table element as Table class attributes.
    row = QTr
    header = QTh
    cell = QTd

    def __init__(
            self,
            columns: list,
            rows: list,
            key: str,
            title: Optional[str] = None,
            selection: Optional[Literal['single', 'multiple', 'none']] = 'none',
            on_filter_change: Optional[Callable] = None,
    ) -> None:
        """QTable

        A component that allows you to display using `QTable <https://quasar.dev/vue-components/table>`_ component.

        :param columns: A list of column objects (see `column API <https://quasar.dev/vue-components/table#qtable-api>`_)
        :param rows: A list of row objects.
        :param key: The name of the column containing unique data identifying the row.
        :param title: The title of the table.
        :param selection: defines the selection behavior.
            'single': only one cell can be selected at a time.
            'multiple': more than one cell can be selected at a time.
            'none': no cells can be selected.

        If selection is passed to 'single' or 'multiple', then a `selected` property is accessible containing
              the selected rows.
        """

        super().__init__(tag='q-table', value='', on_value_change=on_filter_change)

        self._props['columns'] = columns
        self._props['rows'] = rows
        self._props['row-key'] = key
        self._props['title'] = title

        self.selected: list = []
        self._props['selected'] = self.selected
        self._props['selection'] = selection
        self.on('selection', handler=self.on_selection_change)

    def on_selection_change(self, data):
        self.selected = data['args']['rows']
        self._props['selected'] = self.selected
        self.update()
