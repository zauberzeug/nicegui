from typing import Any, Callable, Dict, List, Literal, Optional, Union

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
                 pagination: Optional[Union[int, dict]] = None,
                 on_select: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Table

        A table based on Quasar's `QTable <https://quasar.dev/vue-components/table>`_ component.

        :param columns: list of column objects
        :param rows: list of row objects
        :param row_key: name of the column containing unique data identifying the row (default: "id")
        :param title: title of the table
        :param selection: selection type ("single" or "multiple"; default: `None`)
        :param pagination: A dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means "infinite"; default: `None`).
        :param on_select: callback which is invoked when the selection changes

        If selection is 'single' or 'multiple', then a `selected` property is accessible containing the selected rows.
        """
        super().__init__()

        self._props['columns'] = columns
        self._props['rows'] = rows
        self._props['row-key'] = row_key
        self._props['title'] = title
        self._props['hide-pagination'] = pagination is None
        self._props['pagination'] = pagination if isinstance(pagination, dict) else {'rowsPerPage': pagination or 0}
        self._props['selection'] = selection or 'none'
        self._props['selected'] = []
        self._props['fullscreen'] = False

        def handle_selection(e: GenericEventArguments) -> None:
            if e.args['added']:
                if selection == 'single':
                    self.selected.clear()
                self.selected.extend(e.args['rows'])
            else:
                self.selected = [row for row in self.selected if row[row_key] not in e.args['keys']]
            self.update()
            arguments = TableSelectionEventArguments(sender=self, client=self.client, selection=self.selected)
            handle_event(on_select, arguments)
        self.on('selection', handle_selection, ['added', 'rows', 'keys'])

    @property
    def rows(self) -> List[Dict]:
        """List of rows."""
        return self._props['rows']

    @rows.setter
    def rows(self, value: List[Dict]) -> None:
        self._props['rows'][:] = value
        self.update()

    @property
    def columns(self) -> List[Dict]:
        """List of columns."""
        return self._props['columns']

    @columns.setter
    def columns(self, value: List[Dict]) -> None:
        self._props['columns'][:] = value
        self.update()

    @property
    def row_key(self) -> str:
        """Name of the column containing unique data identifying the row."""
        return self._props['row-key']

    @row_key.setter
    def row_key(self, value: str) -> None:
        self._props['row-key'] = value
        self.update()

    @property
    def selected(self) -> List[Dict]:
        """List of selected rows."""
        return self._props['selected']

    @selected.setter
    def selected(self, value: List[Dict]) -> None:
        self._props['selected'][:] = value
        self.update()

    @property
    def is_fullscreen(self) -> bool:
        """Whether the table is in fullscreen mode."""
        return self._props['fullscreen']

    @is_fullscreen.setter
    def is_fullscreen(self, value: bool) -> None:
        """Set fullscreen mode."""
        self._props['fullscreen'] = value
        self.update()

    def set_fullscreen(self, value: bool) -> None:
        """Set fullscreen mode."""
        self.is_fullscreen = value

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode."""
        self.is_fullscreen = not self.is_fullscreen

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
            """Row Element

            This element is based on Quasar's `QTr <https://quasar.dev/vue-components/table#qtr-api>`_ component.
            """
            super().__init__('q-tr')

    class header(Element):

        def __init__(self) -> None:
            """Header Element

            This element is based on Quasar's `QTh <https://quasar.dev/vue-components/table#qth-api>`_ component.
            """
            super().__init__('q-th')

    class cell(Element):

        def __init__(self) -> None:
            """Cell Element

            This element is based on Quasar's `QTd <https://quasar.dev/vue-components/table#qtd-api>`_ component.
            """
            super().__init__('q-td')
