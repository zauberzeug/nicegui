import importlib.util
from typing import TYPE_CHECKING, Literal, Optional, Union

from typing_extensions import Self

from .. import optional_features
from ..element import Element
from ..events import (
    GenericEventArguments,
    Handler,
    TableSelectionEventArguments,
    ValueChangeEventArguments,
    handle_event,
)
from .mixins.filter_element import FilterElement

if importlib.util.find_spec('pandas'):
    optional_features.register('pandas')
    if TYPE_CHECKING:
        import pandas as pd

if importlib.util.find_spec('polars'):
    optional_features.register('polars')
    if TYPE_CHECKING:
        import polars as pl


class Table(FilterElement, component='table.js'):

    def __init__(self,
                 *,
                 rows: list[dict],
                 columns: Optional[list[dict]] = None,
                 column_defaults: Optional[dict] = None,
                 row_key: str = 'id',
                 title: Optional[str] = None,
                 selection: Literal[None, 'single', 'multiple'] = None,
                 pagination: Optional[Union[int, dict]] = None,
                 on_select: Optional[Handler[TableSelectionEventArguments]] = None,
                 on_pagination_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """Table

        A table based on Quasar's `QTable <https://quasar.dev/vue-components/table>`_ component.

        :param rows: list of row objects
        :param columns: list of column objects (defaults to the columns of the first row *since version 2.0.0*)
        :param column_defaults: optional default column properties, *added in version 2.0.0*
        :param row_key: name of the column containing unique data identifying the row (default: "id")
        :param title: title of the table
        :param selection: selection type ("single" or "multiple"; default: `None`)
        :param pagination: a dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means "infinite"; default: `None`).
        :param on_select: callback which is invoked when the selection changes
        :param on_pagination_change: callback which is invoked when the pagination changes

        If selection is 'single' or 'multiple', then a `selected` property is accessible containing the selected rows.
        """
        super().__init__()

        if columns is None:
            first_row = rows[0] if rows else {}
            columns = [{'name': key, 'label': str(key).upper(), 'field': key, 'sortable': True} for key in first_row]

        self._column_defaults = column_defaults
        self._use_columns_from_df = False
        self._props['columns'] = self._normalize_columns(columns)
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
                if self.selection == 'single':
                    self.selected.clear()
                self.selected.extend(e.args['rows'])
            else:
                self.selected = [row for row in self.selected if row[self.row_key] not in e.args['keys']]
            arguments = TableSelectionEventArguments(sender=self, client=self.client, selection=self.selected)
            for handler in self._selection_handlers:
                handle_event(handler, arguments)
        self.on('selection', handle_selection, ['added', 'rows', 'keys'])

        def handle_pagination_change(e: GenericEventArguments) -> None:
            previous_value = self.pagination
            self.pagination = e.args
            arguments = ValueChangeEventArguments(sender=self, client=self.client,
                                                  value=self.pagination, previous_value=previous_value)
            for handler in self._pagination_change_handlers:
                handle_event(handler, arguments)
        self.on('update:pagination', handle_pagination_change)

    def on_select(self, callback: Handler[TableSelectionEventArguments]) -> Self:
        """Add a callback to be invoked when the selection changes."""
        self._selection_handlers.append(callback)
        return self

    def on_pagination_change(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """Add a callback to be invoked when the pagination changes."""
        self._pagination_change_handlers.append(callback)
        return self

    def _normalize_columns(self, columns: list[dict]) -> list[dict]:
        return [{**self._column_defaults, **column} for column in columns] if self._column_defaults else columns

    @classmethod
    def from_pandas(cls,
                    df: 'pd.DataFrame', *,
                    columns: Optional[list[dict]] = None,
                    column_defaults: Optional[dict] = None,
                    row_key: str = 'id',
                    title: Optional[str] = None,
                    selection: Optional[Literal['single', 'multiple']] = None,
                    pagination: Optional[Union[int, dict]] = None,
                    on_select: Optional[Handler[TableSelectionEventArguments]] = None) -> Self:
        """Create a table from a Pandas DataFrame.

        Note:
        If the DataFrame contains non-serializable columns of type `datetime64[ns]`, `timedelta64[ns]`, `complex128` or `period[M]`,
        they will be converted to strings.
        To use a different conversion, convert the DataFrame manually before passing it to this method.
        See `issue 1698 <https://github.com/zauberzeug/nicegui/issues/1698>`_ for more information.

        *Added in version 2.0.0*

        :param df: Pandas DataFrame
        :param columns: list of column objects (defaults to the columns of the dataframe)
        :param column_defaults: optional default column properties
        :param row_key: name of the column containing unique data identifying the row (default: "id")
        :param title: title of the table
        :param selection: selection type ("single" or "multiple"; default: `None`)
        :param pagination: a dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means "infinite"; default: `None`).
        :param on_select: callback which is invoked when the selection changes
        :return: table element
        """
        rows, columns_from_df = cls._pandas_df_to_rows_and_columns(df)
        table = cls(
            rows=rows,
            columns=columns or columns_from_df,
            column_defaults=column_defaults,
            row_key=row_key,
            title=title,
            selection=selection,
            pagination=pagination,
            on_select=on_select,
        )
        table._use_columns_from_df = columns is None
        return table

    @classmethod
    def from_polars(cls,
                    df: 'pl.DataFrame', *,
                    columns: Optional[list[dict]] = None,
                    column_defaults: Optional[dict] = None,
                    row_key: str = 'id',
                    title: Optional[str] = None,
                    selection: Optional[Literal['single', 'multiple']] = None,
                    pagination: Optional[Union[int, dict]] = None,
                    on_select: Optional[Handler[TableSelectionEventArguments]] = None) -> Self:
        """Create a table from a Polars DataFrame.

        Note:
        If the DataFrame contains non-UTF-8 datatypes, they will be converted to strings.
        To use a different conversion, convert the DataFrame manually before passing it to this method.

        *Added in version 2.7.0*

        :param df: Polars DataFrame
        :param columns: list of column objects (defaults to the columns of the dataframe)
        :param column_defaults: optional default column properties
        :param row_key: name of the column containing unique data identifying the row (default: "id")
        :param title: title of the table
        :param selection: selection type ("single" or "multiple"; default: `None`)
        :param pagination: a dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means "infinite"; default: `None`).
        :param on_select: callback which is invoked when the selection changes
        :return: table element
        """
        rows, columns_from_df = cls._polars_df_to_rows_and_columns(df)
        table = cls(
            rows=rows,
            columns=columns or columns_from_df,
            column_defaults=column_defaults,
            row_key=row_key,
            title=title,
            selection=selection,
            pagination=pagination,
            on_select=on_select,
        )
        table._use_columns_from_df = columns is None
        return table

    def update_from_pandas(self,
                           df: 'pd.DataFrame', *,
                           clear_selection: bool = True,
                           columns: Optional[list[dict]] = None,
                           column_defaults: Optional[dict] = None) -> None:
        """Update the table from a Pandas DataFrame.

        See `from_pandas()` for more information about the conversion of non-serializable columns.

        If `columns` is not provided and the columns had been inferred from a DataFrame,
        the columns will be updated to match the new DataFrame.

        :param df: Pandas DataFrame
        :param clear_selection: whether to clear the selection (default: True)
        :param columns: list of column objects (defaults to the columns of the dataframe)
        :param column_defaults: optional default column properties
        """
        rows, columns_from_df = self._pandas_df_to_rows_and_columns(df)
        self._update_table(rows, columns_from_df, clear_selection, columns, column_defaults)

    def update_from_polars(self,
                           df: 'pl.DataFrame', *,
                           clear_selection: bool = True,
                           columns: Optional[list[dict]] = None,
                           column_defaults: Optional[dict] = None) -> None:
        """Update the table from a Polars DataFrame.

        :param df: Polars DataFrame
        :param clear_selection: whether to clear the selection (default: True)
        :param columns: list of column objects (defaults to the columns of the dataframe)
        :param column_defaults: optional default column properties
        """
        rows, columns_from_df = self._polars_df_to_rows_and_columns(df)
        self._update_table(rows, columns_from_df, clear_selection, columns, column_defaults)

    def _update_table(self,
                      rows: list[dict],
                      columns_from_df: list[dict],
                      clear_selection: bool,
                      columns: Optional[list[dict]],
                      column_defaults: Optional[dict]) -> None:
        """Helper function to update the table."""
        self.rows[:] = rows
        if column_defaults is not None:
            self._column_defaults = column_defaults
        if columns or self._use_columns_from_df:
            self.columns[:] = self._normalize_columns(columns or columns_from_df)
        if clear_selection:
            self.selected.clear()

    @staticmethod
    def _pandas_df_to_rows_and_columns(df: 'pd.DataFrame') -> tuple[list[dict], list[dict]]:
        import pandas as pd  # pylint: disable=import-outside-toplevel

        def is_special_dtype(dtype):
            return (pd.api.types.is_datetime64_any_dtype(dtype) or
                    pd.api.types.is_timedelta64_dtype(dtype) or
                    pd.api.types.is_complex_dtype(dtype) or
                    pd.api.types.is_object_dtype(dtype) or
                    isinstance(dtype, (pd.PeriodDtype, pd.IntervalDtype)))
        special_cols = df.columns[df.dtypes.apply(is_special_dtype)]
        if not special_cols.empty:
            df = df.copy()
            df[special_cols] = df[special_cols].astype(str)

        if isinstance(df.columns, pd.MultiIndex):
            raise ValueError('MultiIndex columns are not supported. '
                             'You can convert them to strings using something like '
                             '`df.columns = ["_".join(col) for col in df.columns.values]`.')

        return df.to_dict('records'), [{'name': col, 'label': col, 'field': col} for col in df.columns]

    @staticmethod
    def _polars_df_to_rows_and_columns(df: 'pl.DataFrame') -> tuple[list[dict], list[dict]]:
        return df.to_dicts(), [{'name': col, 'label': col, 'field': col} for col in df.columns]

    @property
    def rows(self) -> list[dict]:
        """List of rows."""
        return self._props['rows']

    @rows.setter
    def rows(self, value: list[dict]) -> None:
        self._props['rows'] = value

    @property
    def columns(self) -> list[dict]:
        """List of columns."""
        return self._props['columns']

    @columns.setter
    def columns(self, value: list[dict]) -> None:
        self._props['columns'] = self._normalize_columns(value)

    @property
    def column_defaults(self) -> Optional[dict]:
        """Default column properties."""
        return self._column_defaults

    @column_defaults.setter
    def column_defaults(self, value: Optional[dict]) -> None:
        self._column_defaults = value
        self.columns = self.columns  # re-normalize columns

    @property
    def row_key(self) -> str:
        """Name of the column containing unique data identifying the row."""
        return self._props['row-key']

    @row_key.setter
    def row_key(self, value: str) -> None:
        self._props['row-key'] = value

    @property
    def selected(self) -> list[dict]:
        """List of selected rows."""
        return self._props['selected']

    @selected.setter
    def selected(self, value: list[dict]) -> None:
        self._props['selected'] = value

    @property
    def selection(self) -> Literal[None, 'single', 'multiple']:
        """Selection type.

        *Added in version 2.11.0*
        """
        return None if self._props['selection'] == 'none' else self._props['selection']

    @selection.setter
    def selection(self, value: Literal[None, 'single', 'multiple']) -> None:
        self._props['selection'] = value or 'none'

    def set_selection(self, value: Literal[None, 'single', 'multiple']) -> None:
        """Set the selection type.

        *Added in version 2.11.0*
        """
        self.selection = value

    @property
    def pagination(self) -> dict:
        """Pagination object."""
        return self._props['pagination']

    @pagination.setter
    def pagination(self, value: dict) -> None:
        self._props['pagination'] = value

    @property
    def is_fullscreen(self) -> bool:
        """Whether the table is in fullscreen mode."""
        return self._props['fullscreen']

    @is_fullscreen.setter
    def is_fullscreen(self, value: bool) -> None:
        """Set fullscreen mode."""
        self._props['fullscreen'] = value

    def set_fullscreen(self, value: bool) -> None:
        """Set fullscreen mode."""
        self.is_fullscreen = value

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode."""
        self.is_fullscreen = not self.is_fullscreen

    def add_rows(self, rows: list[dict]) -> None:
        """Add rows to the table."""
        self.rows.extend(rows)

    def add_row(self, row: dict) -> None:
        """Add a single row to the table."""
        self.add_rows([row])

    def remove_rows(self, rows: list[dict]) -> None:
        """Remove rows from the table."""
        keys = [row[self.row_key] for row in rows]
        self.rows[:] = [row for row in self.rows if row[self.row_key] not in keys]
        self.selected[:] = [row for row in self.selected if row[self.row_key] not in keys]

    def remove_row(self, row: dict) -> None:
        """Remove a single row from the table."""
        self.remove_rows([row])

    def update_rows(self, rows: list[dict], *, clear_selection: bool = True) -> None:
        """Update rows in the table.

        :param rows: list of rows to update
        :param clear_selection: whether to clear the selection (default: True)
        """
        self.rows[:] = rows
        if clear_selection:
            self.selected.clear()

    async def get_filtered_sorted_rows(self, *, timeout: float = 1) -> list[dict]:
        """Asynchronously return the filtered and sorted rows of the table."""
        return await self.get_computed_prop('filteredSortedRows', timeout=timeout)

    async def get_computed_rows(self, *, timeout: float = 1) -> list[dict]:
        """Asynchronously return the computed rows of the table."""
        return await self.get_computed_prop('computedRows', timeout=timeout)

    async def get_computed_rows_number(self, *, timeout: float = 1) -> int:
        """Asynchronously return the number of computed rows of the table."""
        return await self.get_computed_prop('computedRowsNumber', timeout=timeout)

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
