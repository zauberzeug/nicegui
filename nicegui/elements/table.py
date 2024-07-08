from copy import copy
from typing import Any, Callable, Dict, List, Literal, Optional, TypedDict, Union

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


ColumnsConfigOptions = TypedDict('ColumnsConfigOptions', {
    'align': str,
    'sortable': bool,
    ':sortable': str,
    ':sort': str,
    ':rawSort': str,
    'sortOrder': str,
    ':format': str,
    'style': str,
    ':style': str,
    'classes': str,
    ':classes': str,
    'headerStyle': str,
    'headerClasses': str
},
    total=False)

ColumnsConfig = Dict[str, ColumnsConfigOptions]


def _clean_pandas_dataframe(df: 'pd.DataFrame') -> 'pd.DataFrame':
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
    return df


class Table(FilterElement, component='table.js'):

    def __init__(self,
                 columns: Optional[List[Dict]] = None,
                 rows: Optional[List[Dict]] = None,
                 df: Optional['pd.DataFrame'] = None,
                 default_column: Optional[ColumnsConfigOptions] = None,
                 row_key: str = 'id',
                 title: Optional[str] = None,
                 selection: Optional[Literal['single', 'multiple']] = None,
                 pagination: Optional[Union[int, dict]] = None,
                 on_select: Optional[Callable[..., Any]] = None,
                 on_pagination_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Table

        A table based on Quasar's `QTable <https://quasar.dev/vue-components/table>`_ component.

        :param columns: optional list of column objects. If not provided, column names are inferred from the first row.
        :param rows: list of row objects, one of the two possible sources of rows
        :param df: pandas DataFrame, the other possible sources of rows
        :param default_column: default options which apply to all columns (default: {sortable: True})
        :param row_key: name of the column containing unique data identifying the row (default: "id")
        :param title: title of the table
        :param selection: selection type ("single" or "multiple"; default: `None`)
        :param pagination: a dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means "infinite"; default: `None`).
        :param on_select: callback which is invoked when the selection changes
        :param on_pagination_change: callback which is invoked when the pagination changes

        If selection is 'single' or 'multiple', then a `selected` property is accessible containing the selected rows.
        """
        super().__init__()

        # Columns should be sortable by default
        if default_column is None:
            default_column = {'sortable': True}

        # Keep default_column and columns as separate properties
        self._default_column = default_column
        self._columns = columns
        # Merge them before populating the columns prop
        self._props['columns'] = self._merge_columns_with_default()

        # df and rows are two alternative ways to populate the rows prop
        if df is None and rows is None:
            raise ValueError('You need to provide either rows or df')
        self._df = _clean_pandas_dataframe(df) if df is not None else None
        self._rows = rows
        self._props['rows'] = self._merge_rows_with_dataframe()

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

    @property
    def rows(self) -> List[Dict]:
        """List of rows, which are added to those from 'df'."""
        return self._rows

    @rows.setter
    def rows(self, value: List[Dict]) -> None:
        self._rows = value
        self._props['rows'] = self._merge_rows_with_dataframe()
        self.update()

    @property
    def df(self) -> 'pd.DataFrame':
        """Pandas DataFrame as alternative source of rows, which are added to those of 'rows'."""
        return self._df

    @df.setter
    def df(self, value: 'pd.DataFrame') -> None:
        self._df = _clean_pandas_dataframe(value) if value is not None else None
        self._props['rows'] = self._merge_rows_with_dataframe()
        self.update()

    def _merge_rows_with_dataframe(self) -> Union[List[Dict], None]:
        """Return combined rows resulting from rows merged with dataframe."""
        merged_rows = copy(self._rows) or []
        if self._df is not None:
            merged_rows += self._df.to_dict('records')
        return merged_rows

    @property
    def columns(self) -> List[Dict]:
        """Optional list of columns objects. If not provided, column names are inferred from the first row."""
        return self._columns

    @columns.setter
    def columns(self, value: List[Dict]) -> None:
        self._columns = value
        self._props['columns'] = self._merge_columns_with_default()
        self.update()

    @property
    def default_column(self) -> ColumnsConfigOptions:
        """Optional default column configuration. Default: {'sortable': True}"""
        return self._default_column

    @default_column.setter
    def default_column(self, value: ColumnsConfigOptions) -> None:
        self._default_column = value
        self._props['columns'] = self._merge_columns_with_default()
        self.update()

    def _merge_columns_with_default(self) -> Union[List[Dict], None]:
        """Return columns after applying them defaults from default_column."""
        if self._default_column is not None and self._columns is not None:
            columns = []
            for column in self._columns:
                columns.append({**self._default_column, **column})
            return columns
        return 'none'

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
        self.rows += rows

    def remove_rows(self, *rows: Dict) -> None:
        """Remove rows from the table."""
        keys = [row[self.row_key] for row in rows]
        self._rows = [row for row in self.rows if row[self.row_key] not in keys]
        self._props['rows'] = self._merge_rows_with_dataframe()
        self.selected[:] = [row for row in self.selected if row[self.row_key] not in keys]
        self.update()

    def update_rows(self, rows: List[Dict], *, clear_selection: bool = True) -> None:
        """Update rows in the table.

        :param rows: list of rows to update
        :param clear_selection: whether to clear the selection (default: True)
        """
        self._rows = rows
        self._props['rows'] = self._merge_rows_with_dataframe()
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
