import importlib.util
from typing import TYPE_CHECKING, Any, Literal

from typing_extensions import Self

from .. import optional_features
from ..defaults import DEFAULT_PROP, resolve_defaults
from ..element import Element
from ..events import (
    GenericEventArguments,
    Handler,
    TableSelectionEventArguments,
    ValueChangeEventArguments,
    handle_event,
)
from ..logging import log
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

    @resolve_defaults
    def __init__(self,
                 *,
                 rows: list[dict],
                 columns: list[dict] | None = None,
                 column_defaults: dict | None = None,
                 row_key: str = DEFAULT_PROP | 'id',
                 title: str | None = DEFAULT_PROP | None,
                 selection: Literal[None, 'single', 'multiple'] = DEFAULT_PROP | None,
                 pagination: int | dict | None = None,
                 on_select: Handler[TableSelectionEventArguments] | None = None,
                 on_pagination_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Table

        A table based on Quasar's `QTable <https://quasar.dev/vue-components/table>`_ component.
        Updates can be pushed to the table by updating the ``rows`` or ``columns`` properties.

        If ``selection`` is "single" or "multiple", then a ``selected`` property is accessible containing the selected rows.

        Note:
        Cells in ``rows`` must not contain lists because they can cause the browser to crash.
        To display complex data structures, convert them to strings first (e.g., using ``str()`` or custom formatting).

        :param rows: list of row objects
        :param columns: list of column objects (defaults to the columns of the first row *since version 2.0.0*)
        :param column_defaults: optional default column properties, *added in version 2.0.0*
        :param row_key: name of the column containing unique data identifying the row (default: "id")
        :param title: title of the table
        :param selection: selection type ("single" or "multiple"; default: `None`)
        :param pagination: a dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means "infinite"; default: `None`).
        :param on_select: callback which is invoked when the selection changes
        :param on_pagination_change: callback which is invoked when the pagination changes
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
        self._props.set_optional('title', title)
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

    def _to_dict(self) -> dict[str, Any]:
        # scan rows for lists and add slot templates if needed
        for column in self._props['columns']:
            field = column.get('field')
            name = column.get('name')
            if not field or not name or f'body-cell-{name}' in self.slots:
                continue
            for row in self._props['rows']:
                value = row.get(field)
                if isinstance(value, (list, set, tuple)):
                    log.warning(
                        f'Found list in column "{name}": {value}.\n'
                        'Unless there is slot template, table rows must not contain lists or the browser will crash.\n'
                        'NiceGUI is intervening by adding a slot template to display the list as comma-separated values.'
                    )
                    self.add_slot(f'body-cell-{name}', '''
                        <td class="text-right" :props="props">
                            {{ Array.isArray(props.value) ? props.value.join(', ') : props.value }}
                        </td>
                    ''')
                    break

        return super()._to_dict()

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
                    columns: list[dict] | None = None,
                    column_defaults: dict | None = None,
                    row_key: str = 'id',
                    title: str | None = None,
                    selection: Literal['single', 'multiple'] | None = None,
                    pagination: int | dict | None = None,
                    on_select: Handler[TableSelectionEventArguments] | None = None) -> Self:
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
                    columns: list[dict] | None = None,
                    column_defaults: dict | None = None,
                    row_key: str = 'id',
                    title: str | None = None,
                    selection: Literal['single', 'multiple'] | None = None,
                    pagination: int | dict | None = None,
                    on_select: Handler[TableSelectionEventArguments] | None = None) -> Self:
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
                           columns: list[dict] | None = None,
                           column_defaults: dict | None = None) -> None:
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
                           columns: list[dict] | None = None,
                           column_defaults: dict | None = None) -> None:
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
                      columns: list[dict] | None,
                      column_defaults: dict | None) -> None:
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
    def column_defaults(self) -> dict | None:
        """Default column properties."""
        return self._column_defaults

    @column_defaults.setter
    def column_defaults(self, value: dict | None) -> None:
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

    class header(Element, default_classes='[&>*]:inline'):

        def __init__(self, column_name: str | None = None) -> None:
            """Header Element

            This element is based on Quasar's `QTh <https://quasar.dev/vue-components/table#qth-api>`_ component.

            :param column_name: corresponding column to access alignment and other properties (*added in version 3.5.0*)
            """
            super().__init__('q-th')
            if column_name is not None:
                self._props[':props'] = 'props'
                self._props['key'] = column_name

    class cell(Element):

        def __init__(self, column_name: str | None = None) -> None:
            """Cell Element

            This element is based on Quasar's `QTd <https://quasar.dev/vue-components/table#qtd-api>`_ component.

            :param column_name: corresponding column to access alignment and other properties (*added in version 3.5.0*)
            """
            super().__init__('q-td')
            if column_name is not None:
                self._props[':props'] = 'props'
                self._props['key'] = column_name
