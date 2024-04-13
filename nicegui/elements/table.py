from typing import Any, Callable, Dict, List, Literal, Optional, Union

from typing_extensions import Self

from .. import optional_features
from ..element import Element
from ..events import GenericEventArguments, TableSelectionEventArguments, ValueChangeEventArguments, handle_event
from .mixins.filter_element import FilterElement

try:
    import pandas as pd
    optional_features.register('pandas')
except ImportError:
    pass


class Table(FilterElement, component='table.js'):

    def __init__(self,
                 columns: List[Dict],
                 rows: List[Dict],
                 row_key: str = 'id',
                 title: Optional[str] = None,
                 selection: Optional[Literal['single', 'multiple']] = None,
                 pagination: Optional[Union[int, dict]] = None,
                 on_select: Optional[Callable[..., Any]] = None,
                 on_pagination_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Table

        A table based on Quasar's `QTable <https://quasar.dev/vue-components/table>`_ component.

        :param columns: list of column objects
        :param rows: list of row objects
        :param row_key: name of the column containing unique data identifying the row (default: "id")
        :param title: title of the table
        :param selection: selection type ("single" or "multiple"; default: `None`)
        :param pagination: a dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means "infinite"; default: `None`).
        :param on_select: callback which is invoked when the selection changes
        :param on_pagination_change: callback which is invoked when the pagination changes

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
        self._selection_handlers = [on_select] if on_select else []
        self._pagination_change_handlers = [on_pagination_change] if on_pagination_change else []

        def handle_selection(e: GenericEventArguments) -> None:
            if e.args['added']:
                if selection == 'single':
                    self.selected.clear()
                self.selected.extend(e.args['rows'])
            else:
                self.selected = [row for row in self.selected if row[row_key] not in e.args['keys']]
            self.update()
            arguments = TableSelectionEventArguments(sender=self, client=self.client, selection=self.selected)
            for handler in self._selection_handlers:
                handle_event(handler, arguments)
        self.on('selection', handle_selection, ['added', 'rows', 'keys'])

        def handle_pagination_change(e: GenericEventArguments) -> None:
            self.pagination = e.args
            self.update()
            arguments = ValueChangeEventArguments(sender=self, client=self.client, value=self.pagination)
            for handler in self._pagination_change_handlers:
                handle_event(handler, arguments)
        self.on('update:pagination', handle_pagination_change)

    def on_select(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when the selection changes."""
        self._selection_handlers.append(callback)
        return self

    def on_pagination_change(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when the pagination changes."""
        self._pagination_change_handlers.append(callback)
        return self

    @classmethod
    def from_pandas(cls,
                    df: 'pd.DataFrame',
                    row_key: str = 'id',
                    title: Optional[str] = None,
                    selection: Optional[Literal['single', 'multiple']] = None,
                    pagination: Optional[Union[int, dict]] = None,
                    on_select: Optional[Callable[..., Any]] = None) -> Self:
        """Create a table from a Pandas DataFrame.

        Note:
        If the DataFrame contains non-serializable columns of type `datetime64[ns]`, `timedelta64[ns]`, `complex128` or `period[M]`,
        they will be converted to strings.
        To use a different conversion, convert the DataFrame manually before passing it to this method.
        See `issue 1698 <https://github.com/zauberzeug/nicegui/issues/1698>`_ for more information.

        :param df: Pandas DataFrame
        :param row_key: name of the column containing unique data identifying the row (default: "id")
        :param title: title of the table
        :param selection: selection type ("single" or "multiple"; default: `None`)
        :param pagination: a dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means "infinite"; default: `None`).
        :param on_select: callback which is invoked when the selection changes
        :return: table element
        """
        def is_special_dtype(dtype):
            return (pd.api.types.is_datetime64_any_dtype(dtype) or
                    pd.api.types.is_timedelta64_dtype(dtype) or
                    pd.api.types.is_complex_dtype(dtype) or
                    isinstance(dtype, pd.PeriodDtype))
        special_cols = df.columns[df.dtypes.apply(is_special_dtype)]
        if not special_cols.empty:
            df = df.copy()
            df[special_cols] = df[special_cols].astype(str)

        if isinstance(df.columns, pd.MultiIndex):
            raise ValueError('MultiIndex columns are not supported. '
                             'You can convert them to strings using something like '
                             '`df.columns = ["_".join(col) for col in df.columns.values]`.')

        return cls(
            columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
            rows=df.to_dict('records'),
            row_key=row_key,
            title=title,
            selection=selection,
            pagination=pagination,
            on_select=on_select)

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
    def pagination(self) -> dict:
        """Pagination object."""
        return self._props['pagination']

    @pagination.setter
    def pagination(self, value: dict) -> None:
        self._props['pagination'] = value
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

    def update_rows(self, rows: List[Dict], *, clear_selection: bool = True) -> None:
        """Update rows in the table.

        :param rows: list of rows to update
        :param clear_selection: whether to clear the selection (default: True)
        """
        self.rows[:] = rows
        if clear_selection:
            self.selected.clear()
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
