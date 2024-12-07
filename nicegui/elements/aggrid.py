import importlib.util
from typing import TYPE_CHECKING, Dict, List, Literal, Optional, cast

from typing_extensions import Self

from .. import helpers, optional_features
from ..awaitable_response import AwaitableResponse
from ..element import Element

if importlib.util.find_spec('pandas'):
    optional_features.register('pandas')
    if TYPE_CHECKING:
        import pandas as pd

if importlib.util.find_spec('polars'):
    optional_features.register('polars')
    if TYPE_CHECKING:
        import polars as pl


class AgGrid(Element,
             component='aggrid.js',
             dependencies=['lib/aggrid/ag-grid-community.min.js'],
             default_classes='nicegui-aggrid'):

    def __init__(self,
                 options: Dict, *,
                 html_columns: List[int] = [],  # noqa: B006
                 theme: str = 'balham',
                 auto_size_columns: bool = True,
                 ) -> None:
        """AG Grid

        An element to create a grid using `AG Grid <https://www.ag-grid.com/>`_.

        The methods `run_grid_method` and `run_row_method` can be used to interact with the AG Grid instance on the client.

        :param options: dictionary of AG Grid options
        :param html_columns: list of columns that should be rendered as HTML (default: `[]`)
        :param theme: AG Grid theme (default: 'balham')
        :param auto_size_columns: whether to automatically resize columns to fit the grid width (default: `True`)
        """
        super().__init__()
        self._props['options'] = options
        self._props['html_columns'] = html_columns[:]
        self._props['auto_size_columns'] = auto_size_columns
        self._classes.append(f'ag-theme-{theme}')

    @classmethod
    def from_pandas(cls,
                    df: 'pd.DataFrame', *,
                    theme: str = 'balham',
                    auto_size_columns: bool = True,
                    options: Dict = {}) -> Self:  # noqa: B006
        """Create an AG Grid from a Pandas DataFrame.

        Note:
        If the DataFrame contains non-serializable columns of type `datetime64[ns]`, `timedelta64[ns]`, `complex128` or `period[M]`,
        they will be converted to strings.
        To use a different conversion, convert the DataFrame manually before passing it to this method.
        See `issue 1698 <https://github.com/zauberzeug/nicegui/issues/1698>`_ for more information.

        :param df: Pandas DataFrame
        :param theme: AG Grid theme (default: 'balham')
        :param auto_size_columns: whether to automatically resize columns to fit the grid width (default: `True`)
        :param options: dictionary of additional AG Grid options
        :return: AG Grid element
        """
        import pandas as pd  # pylint: disable=import-outside-toplevel

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

        return cls({
            'columnDefs': [{'field': str(col)} for col in df.columns],
            'rowData': df.to_dict('records'),
            'suppressFieldDotNotation': True,
            **options,
        }, theme=theme, auto_size_columns=auto_size_columns)

    @classmethod
    def from_polars(cls,
                    df: 'pl.DataFrame', *,
                    theme: str = 'balham',
                    auto_size_columns: bool = True,
                    options: Dict = {}) -> Self:  # noqa: B006
        """Create an AG Grid from a Polars DataFrame.

        If the DataFrame contains non-UTF-8 datatypes, they will be converted to strings.
        To use a different conversion, convert the DataFrame manually before passing it to this method.

        :param df: Polars DataFrame
        :param theme: AG Grid theme (default: 'balham')
        :param auto_size_columns: whether to automatically resize columns to fit the grid width (default: `True`)
        :param options: dictionary of additional AG Grid options
        :return: AG Grid element
        """
        return cls({
            'columnDefs': [{'field': str(col)} for col in df.columns],
            'rowData': df.to_dicts(),
            'suppressFieldDotNotation': True,
            **options,
        }, theme=theme, auto_size_columns=auto_size_columns)

    @property
    def options(self) -> Dict:
        """The options dictionary."""
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_grid')

    def run_grid_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """Run an AG Grid API method.

        See `AG Grid API <https://www.ag-grid.com/javascript-data-grid/grid-api/>`_ for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method
        :param args: arguments to pass to the method
        :param timeout: timeout in seconds (default: 1 second)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('run_grid_method', name, *args, timeout=timeout)

    def run_column_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:  # DEPRECATED
        """This method is deprecated. Use `run_grid_method` instead.

        See https://www.ag-grid.com/javascript-data-grid/column-api/ for more information
        """
        helpers.warn_once('The method `run_column_method` is deprecated. '
                          'It will be removed in NiceGUI 3.0. '
                          'Use `run_grid_method` instead.')
        return self.run_method('run_grid_method', name, *args, timeout=timeout)

    def run_row_method(self, row_id: str, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """Run an AG Grid API method on a specific row.

        See `AG Grid Row Reference <https://www.ag-grid.com/javascript-data-grid/row-object/>`_ for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param row_id: id of the row (as defined by the ``getRowId`` option)
        :param name: name of the method
        :param args: arguments to pass to the method
        :param timeout: timeout in seconds (default: 1 second)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('run_row_method', row_id, name, *args, timeout=timeout)

    async def get_selected_rows(self) -> List[Dict]:
        """Get the currently selected rows.

        This method is especially useful when the grid is configured with ``rowSelection: 'multiple'``.

        See `AG Grid API <https://www.ag-grid.com/javascript-data-grid/row-selection/#reference-selection-getSelectedRows>`_ for more information.

        :return: list of selected row data
        """
        result = await self.run_grid_method('getSelectedRows')
        return cast(List[Dict], result)

    async def get_selected_row(self) -> Optional[Dict]:
        """Get the single currently selected row.

        This method is especially useful when the grid is configured with ``rowSelection: 'single'``.

        :return: row data of the first selection if any row is selected, otherwise `None`
        """
        rows = await self.get_selected_rows()
        return rows[0] if rows else None

    async def get_client_data(
        self,
        *,
        timeout: float = 1,
        method: Literal['all_unsorted', 'filtered_unsorted', 'filtered_sorted', 'leaf'] = 'all_unsorted'
    ) -> List[Dict]:
        """Get the data from the client including any edits made by the client.

        This method is especially useful when the grid is configured with ``'editable': True``.

        See `AG Grid API <https://www.ag-grid.com/javascript-data-grid/accessing-data/>`_ for more information.

        Note that when editing a cell, the row data is not updated until the cell exits the edit mode.
        This does not happen when the cell loses focus, unless ``stopEditingWhenCellsLoseFocus: True`` is set.

        :param timeout: timeout in seconds (default: 1 second)
        :param method: method to access the data, "all_unsorted" (default), "filtered_unsorted", "filtered_sorted", "leaf"

        :return: list of row data
        """
        API_METHODS = {
            'all_unsorted': 'forEachNode',
            'filtered_unsorted': 'forEachNodeAfterFilter',
            'filtered_sorted': 'forEachNodeAfterFilterAndSort',
            'leaf': 'forEachLeafNode',
        }
        result = await self.client.run_javascript(f'''
            const rowData = [];
            getElement({self.id}).api.{API_METHODS[method]}(node => rowData.push(node.data));
            return rowData;
        ''', timeout=timeout)
        return cast(List[Dict], result)

    async def load_client_data(self) -> None:
        """Obtain client data and update the element's row data with it.

        This syncs edits made by the client in editable cells to the server.

        Note that when editing a cell, the row data is not updated until the cell exits the edit mode.
        This does not happen when the cell loses focus, unless ``stopEditingWhenCellsLoseFocus: True`` is set.
        """
        client_row_data = await self.get_client_data()
        self.options['rowData'] = client_row_data
        self.update()
