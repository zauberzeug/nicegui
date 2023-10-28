from __future__ import annotations

from typing import Dict, List, Optional, cast

from .. import optional_features
from ..awaitable_response import AwaitableResponse
from ..element import Element

try:
    import pandas as pd
    optional_features.register('pandas')
except ImportError:
    pass


class AgGrid(Element, component='aggrid.js', libraries=['lib/aggrid/ag-grid-community.min.js']):

    def __init__(self,
                 options: Dict, *,
                 html_columns: List[int] = [],
                 theme: str = 'balham',
                 auto_size_columns: bool = True,
                 ) -> None:
        """AG Grid

        An element to create a grid using `AG Grid <https://www.ag-grid.com/>`_.

        The methods `call_api_method` and `call_column_api_method` can be used to interact with the AG Grid instance on the client.

        :param options: dictionary of AG Grid options
        :param html_columns: list of columns that should be rendered as HTML (default: `[]`)
        :param theme: AG Grid theme (default: 'balham')
        :param auto_size_columns: whether to automatically resize columns to fit the grid width (default: `True`)
        """
        super().__init__()
        self._props['options'] = options
        self._props['html_columns'] = html_columns
        self._props['auto_size_columns'] = auto_size_columns
        self._classes = ['nicegui-aggrid', f'ag-theme-{theme}']

    @staticmethod
    def from_pandas(df: pd.DataFrame, *,
                    theme: str = 'balham',
                    auto_size_columns: bool = True,
                    options: Dict = {}) -> AgGrid:
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
        date_cols = df.columns[df.dtypes == 'datetime64[ns]']
        time_cols = df.columns[df.dtypes == 'timedelta64[ns]']
        complex_cols = df.columns[df.dtypes == 'complex128']
        period_cols = df.columns[df.dtypes == 'period[M]']
        if len(date_cols) != 0 or len(time_cols) != 0 or len(complex_cols) != 0 or len(period_cols) != 0:
            df = df.copy()
            df[date_cols] = df[date_cols].astype(str)
            df[time_cols] = df[time_cols].astype(str)
            df[complex_cols] = df[complex_cols].astype(str)
            df[period_cols] = df[period_cols].astype(str)

        return AgGrid({
            'columnDefs': [{'field': str(col)} for col in df.columns],
            'rowData': df.to_dict('records'),
            'suppressDotNotation': True,
            **options,
        }, theme=theme, auto_size_columns=auto_size_columns)

    @property
    def options(self) -> Dict:
        """The options dictionary."""
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_grid')

    def call_api_method(self, name: str, *args) -> AwaitableResponse:
        """Call an AG Grid API method.

        See `AG Grid API <https://www.ag-grid.com/javascript-data-grid/grid-api/>`_ for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method
        :param args: arguments to pass to the method

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('call_api_method', name, *args)

    def call_column_api_method(self, name: str, *args) -> AwaitableResponse:
        """Call an AG Grid Column API method.

        See `AG Grid Column API <https://www.ag-grid.com/javascript-data-grid/column-api/>`_ for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method
        :param args: arguments to pass to the method

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('call_column_api_method', name, *args)

    async def get_selected_rows(self) -> List[Dict]:
        """Get the currently selected rows.

        This method is especially useful when the grid is configured with ``rowSelection: 'multiple'``.

        See `AG Grid API <https://www.ag-grid.com/javascript-data-grid/row-selection/#reference-selection-getSelectedRows>`_ for more information.

        :return: list of selected row data
        """
        result = await self.call_api_method('getSelectedRows')
        return cast(List[Dict], result)

    async def get_selected_row(self) -> Optional[Dict]:
        """Get the single currently selected row.

        This method is especially useful when the grid is configured with ``rowSelection: 'single'``.

        :return: row data of the first selection if any row is selected, otherwise `None`
        """
        rows = await self.get_selected_rows()
        return rows[0] if rows else None

    async def get_client_data(self) -> List[Dict]:
        """Get the data from the client including any edits made by the client.

        This method is especially useful when the grid is configured with ``'editable': True``.

        See `AG Grid API <https://www.ag-grid.com/javascript-data-grid/accessing-data/>`_ for more information.

        Note that when editing a cell, the row data is not updated until the cell exits the edit mode.
        This does not happen when the cell loses focus, unless ``stopEditingWhenCellsLoseFocus: True`` is set.

        :return: list of row data
        """
        result = await self.client.run_javascript(f'''
            const rowData = [];
            getElement({self.id}).gridOptions.api.forEachNode(node => rowData.push(node.data));
            return rowData;
        ''')
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
