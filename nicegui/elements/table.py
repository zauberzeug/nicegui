from typing import Any, Callable, Dict, List, Optional

from typing_extensions import Literal

from ..element import Element
from ..events import GenericEventArguments, TableSelectionEventArguments, handle_event
from .mixins.filter_element import FilterElement


class Table(FilterElement, component='table.js'):

    def __init__(self,
                 columns: List[Dict],
                 rows: List[Dict],
                 row_key: str = 'id',
                 title: Optional[str] = None,
                 selection: Optional[Literal['single', 'multiple']] = None,
                 pagination: Optional[int] = None,
                 on_select: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Table

        A table based on Quasar's `QTable <https://quasar.dev/vue-components/table>`_ component.

        :param columns: list of column objects
        :param rows: list of row objects
        :param row_key: name of the column containing unique data identifying the row (default: "id")
        :param title: title of the table
        :param selection: selection type ("single" or "multiple"; default: `None`)
        :param pagination: number of rows per page (`None` hides the pagination, 0 means "infinite"; default: `None`)
        :param on_select: callback which is invoked when the selection changes

        If selection is 'single' or 'multiple', then a `selected` property is accessible containing the selected rows.
        """
        super().__init__()

        self.rows = rows
        self.row_key = row_key
        self.selected: List[Dict] = []

        self._props['columns'] = columns
        self._props['rows'] = rows
        self._props['row-key'] = row_key
        self._props['title'] = title
        self._props['hide-pagination'] = pagination is None
        self._props['pagination'] = {'rowsPerPage': pagination or 0}
        self._props['selection'] = selection or 'none'
        self._props['selected'] = self.selected

        def handle_selection(e: GenericEventArguments) -> None:
            if e.args['added']:
                if selection == 'single':
                    self.selected.clear()
                self.selected.extend(e.args['rows'])
            else:
                self.selected[:] = [row for row in self.selected if row[row_key] not in e.args['keys']]
            self.update()
            arguments = TableSelectionEventArguments(sender=self, client=self.client, selection=self.selected)
            handle_event(on_select, arguments)
        self.on('selection', handle_selection, ['added', 'rows', 'keys'])

    def add_rows(self, *rows: Dict) -> None:
        """Add rows to the table."""
        self.rows.extend(rows)
        self.update()

    def remove_rows(self, *rows: Dict) -> None:
        """Remove rows from the table."""
        keys = [row[self.row_key] for row in rows]
        self.rows[:] = [row for row in self.rows if row[self.row_key] not in keys]
        self.selected[:] = [row for row in self.selected if row[self.row_key] not in keys]
        self.update()

    class row(Element):
        def __init__(self) -> None:
            super().__init__('q-tr')

    class header(Element):
        def __init__(self) -> None:
            super().__init__('q-th')

    class cell(Element):
        def __init__(self, key: str = '') -> None:
            super().__init__('q-td')
            if key:
                self._props['key'] = key
