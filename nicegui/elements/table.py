from typing import Any, Dict, Optional

from typing_extensions import Literal

from .mixins.filter_element import FilterElement
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


class QTable(ValueElement, FilterElement):
    row = QTr
    header = QTh
    cell = QTd

    VALUE_PROP = 'selected'
    EVENT_ARGS = None
    EVENT = 'selection'
    def __init__(
            self,
            columns: list,
            rows: list,
            key: str,
            title: Optional[str] = None,
            selection: Optional[Literal['single', 'multiple', 'none']] = 'none',
            pagination: Optional[int] = 0,
    ) -> None:
        """QTable

        A component that allows you to display using `QTable <https://quasar.dev/vue-components/table>`_ component.

        :param columns: A list of column objects (see `column API <https://quasar.dev/vue-components/table#qtable-api>`_)
        :param rows: A list of row objects.
        :param key: The name of the column containing unique data identifying the row.
        :param title: The title of the table.
        :param selection: defines the selection behavior (default= 'none').
            'single': only one cell can be selected at a time.
            'multiple': more than one cell can be selected at a time.
            'none': no cells can be selected.
        :param pagination: defines the number of rows per page. Explicitly set to None to hide pagination (default = 0).

        If selection is passed to 'single' or 'multiple', then a `selected` property is accessible containing
              the selected rows.
        """

        super().__init__(tag='q-table', value=[], on_value_change=None)

        self._props['columns'] = columns
        self._props['rows'] = rows
        self._props['row-key'] = key
        self._props['title'] = title

        if pagination is None:
            self._props['hide-pagination'] = True
            pagination = 0
        self._props['pagination'] = {
            'rowsPerPage': pagination
        }

        self.selected: list = []
        self._props['selection'] = selection

    def _msg_to_value(self, msg: Dict) -> Any:
        self.selected = msg['args']
        return msg['args']['rows']
