from typing import Dict, List, Optional, cast

from typing_extensions import Self

from .. import optional_features
from ..awaitable_response import AwaitableResponse
from ..element import Element

try:
    import pandas as pd
    optional_features.register('pandas')
except ImportError:
    pass


class AgGrid(Element, component='aggrid.js', libraries=['lib/aggrid/ag-grid-community.min.js']):
    """AG Grid

    An element to create a grid using [AG Grid](https://www.ag-grid.com/).

    The `AgGrid` class represents a grid element that can be used to display tabular data using the AG Grid library.
    It provides methods to interact with the grid instance on the client side.

    Args:
    
        - options (Dict): Dictionary of AG Grid options.
        - html_columns (List[int], optional): List of columns that should be rendered as HTML. Defaults to [].
        - theme (str, optional): AG Grid theme. Defaults to 'balham'.
        - auto_size_columns (bool, optional): Whether to automatically resize columns to fit the grid width. Defaults to True.

    Attributes:
        - options (Dict): The options dictionary.

    Methods:
        - from_pandas(cls, df, theme='balham', auto_size_columns=True, options={}) -> AgGrid:
            Create an AG Grid from a Pandas DataFrame.

        - update(self) -> None:
            Update the grid.

        - run_grid_method(self, name, *args, timeout=1, check_interval=0.01) -> AwaitableResponse:
            Run an AG Grid API method.

        - run_column_method(self, name, *args, timeout=1, check_interval=0.01) -> AwaitableResponse:
            Run an AG Grid Column API method.

        - run_row_method(self, row_id, name, *args, timeout=1, check_interval=0.01) -> AwaitableResponse:
            Run an AG Grid API method on a specific row.

        - get_selected_rows(self) -> List[Dict]:
            Get the currently selected rows.

        - get_selected_row(self) -> Optional[Dict]:
            Get the single currently selected row.

        - get_client_data(self, timeout=1, check_interval=0.01) -> List[Dict]:
            Get the data from the client including any edits made by the client.

        - load_client_data(self) -> None:
            Obtain client data and update the element's row data with it.
    """

    def __init__(self,
                 options: Dict, *,
                 html_columns: List[int] = [],
                 theme: str = 'balham',
                 auto_size_columns: bool = True,
                 ) -> None:
        """AG Grid

        An element to create a grid using [AG Grid ](https://www.ag-grid.com/).

        The methods `run_grid_method` and `run_column_method` can be used to interact with the AG Grid instance on the client.

        Args:
        
            - options (Dict): Dictionary of AG Grid options.
            - html_columns (List[int], optional): List of columns that should be rendered as HTML. Defaults to [].
            - theme (str, optional): AG Grid theme. Defaults to 'balham'.
            - auto_size_columns (bool, optional): Whether to automatically resize columns to fit the grid width. Defaults to True.
        """
        super().__init__()
        self._props['options'] = options
        self._props['html_columns'] = html_columns
        self._props['auto_size_columns'] = auto_size_columns
        self._classes.append('nicegui-aggrid')
        self._classes.append(f'ag-theme-{theme}')

    @classmethod
    def from_pandas(cls,
                    df: 'pd.DataFrame', *,
                    theme: str = 'balham',
                    auto_size_columns: bool = True,
                    options: Dict = {}) -> Self:
        """Create an AG Grid from a Pandas DataFrame.

        Note:
            If the DataFrame contains non-serializable columns of type `datetime64[ns]`, `timedelta64[ns]`, `complex128` or `period[M]`,
            they will be converted to strings.
            To use a different conversion, convert the DataFrame manually before passing it to this method.
            See [issue 1698](https://github.com/zauberzeug/nicegui/issues/1698) for more information.

        Args:
        
            - df (pd.DataFrame): Pandas DataFrame.
            - theme (str, optional): AG Grid theme. Defaults to 'balham'.
            - auto_size_columns (bool, optional): Whether to automatically resize columns to fit the grid width. Defaults to True.
            - options (Dict, optional): Dictionary of additional AG Grid options.

        Returns:
            - AgGrid: AG Grid element.
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

        if isinstance(df.columns, pd.MultiIndex):
            raise ValueError('MultiIndex columns are not supported. '
                             'You can convert them to strings using something like '
                             '`df.columns = ["_".join(col) for col in df.columns.values]`.')

        return cls({
            'columnDefs': [{'field': str(col)} for col in df.columns],
            'rowData': df.to_dict('records'),
            'suppressDotNotation': True,
            **options,
        }, theme=theme, auto_size_columns=auto_size_columns)

    @property
    def options(self) -> Dict:
            """
            Get the options dictionary.

            Returns:
                dict: The options dictionary containing configuration options for the AgGrid element.

            Examples:
                >>> grid = AgGrid()
                >>> options = grid.options()
                >>> print(options)
                {'option1': value1, 'option2': value2, ...}

            Note:
                The options dictionary allows you to customize the behavior and appearance of the AgGrid element.
                You can set various configuration options such as column definitions, sorting, filtering, pagination, etc.
                For more details, refer to the AgGrid documentation: [AgGrid Options](https://www.ag-grid.com/javascript-grid-properties/).
            """
            return self._props['options']

    def update(self) -> None:
            """
            Update the grid.

            This method updates the grid by calling the base class's update method and then running the 'update_grid'
            method. It should be called whenever the grid needs to be refreshed with new data or changes.

            Usage:
                grid = AGGrid()
                grid.update()

            Note:
                - This method should be called after making any changes to the grid's data or configuration.
                - The 'update_grid' method is responsible for updating the grid's visual representation based on the
                  current data and configuration.
            """
            super().update()
            self.run_method('update_grid')

    def call_api_method(self, name: str, *args, timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
        """
        DEPRECATED: Use `run_grid_method` instead.

        Calls an API method with the given name and arguments asynchronously.

        Args:
        
            - name (str): The name of the API method to call.
            - *args: Variable length argument list to be passed to the API method.
            - timeout (float, optional): The maximum time to wait for the API method to complete (in seconds). Defaults to 1.
            - check_interval (float, optional): The interval at which to check if the API method has completed (in seconds). Defaults to 0.01.

        Returns:
            - AwaitableResponse: An awaitable response object that can be used to wait for the API method to complete.

        Raises:
            - None
        """
        return self.run_grid_method(name, *args, timeout=timeout, check_interval=check_interval)

    def run_grid_method(self, name: str, *args, timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
            """Run an AG Grid API method.

            This method allows you to execute a method from the AG Grid API. The AG Grid API provides a set of methods that can be used to interact with the grid, such as sorting, filtering, and updating data.

            You can find a list of available methods in the [AG Grid API documentation](https://www.ag-grid.com/javascript-data-grid/grid-api/).

            If the function is awaited, the result of the method call is returned. Otherwise, the method is executed without waiting for a response.

            Args:
                - name (str): The name of the method to be executed.
                - args: The arguments to pass to the method.
                - timeout (float, optional): The timeout in seconds for waiting for a response. Defaults to 1 second.
                - check_interval (float, optional): The interval in seconds to check for a response. Defaults to 0.01 seconds.

            Returns:
                AwaitableResponse: An AwaitableResponse object that can be awaited to get the result of the method call.

            Example:
                ```
                # Create an instance of the AG Grid
                grid = AGGrid()

                # Run the 'sort' method on the grid
                response = grid.run_grid_method('sort', 'column_name', 'asc')

                # Wait for the response
                result = await response

                # Process the result
                if result.success:
                    print('Method executed successfully')
                else:
                    print('Method execution failed')
                ```
            """
            return self.run_method('run_grid_method', name, *args, timeout=timeout, check_interval=check_interval)

    def call_column_method(self, name: str, *args, timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
            """
            DEPRECATED: Use `run_column_method` instead.

            Calls a method on each column in the grid.

            Args:
                - name (str): The name of the method to call on each column.
                - *args: Variable length argument list to be passed to the method.
                - timeout (float, optional): The maximum time to wait for the method to complete (in seconds). Defaults to 1.
                - check_interval (float, optional): The interval between checks for method completion (in seconds). Defaults to 0.01.

            Returns:
                - AwaitableResponse: An awaitable response object that can be used to wait for the method to complete.

            Raises:
                None.

            Example:
                To call the `sort` method on each column in the grid:

                ```python
                response = call_column_method('sort')
                await response
                ```

            Note:
                This method is deprecated. Please use `run_column_method` instead.
            """
            return self.run_column_method(name, *args, timeout=timeout, check_interval=check_interval)

    def run_column_method(self, name: str, *args,
                              timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
            """Run an AG Grid Column API method.

            This method allows you to execute a method from the AG Grid Column API. The AG Grid Column API provides a set of methods
            that allow you to interact with the columns in the AG Grid.

            You can find a list of available methods in the [AG Grid Column API documentation](https://www.ag-grid.com/javascript-data-grid/column-api/).

            If the function is awaited, the result of the method call is returned. Otherwise, the method is executed without waiting for a response.

            Args:
            
                - name (str): The name of the method to be executed.
                - args: The arguments to be passed to the method.
                - timeout (float, optional): The timeout in seconds for waiting for a response. Defaults to 1 second.
                - check_interval (float, optional): The interval in seconds to check for a response. Defaults to 0.01 seconds.

            Returns:
                - AwaitableResponse: An AwaitableResponse object that can be awaited to get the result of the method call.

            Example usage:
                ```
                # Create an instance of AGGrid class
                ag_grid = AGGrid()

                # Run a column method
                response = ag_grid.run_column_method('setColumnVisible', 'columnId', False)

                # Await the response to get the result
                result = await response
                ```
            """
            return self.run_method('run_column_method', name, *args, timeout=timeout, check_interval=check_interval)

    def run_row_method(self, row_id: str, name: str, *args,
                           timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
            """Run an AG Grid API method on a specific row.

            This method allows you to execute an AG Grid API method on a specific row identified by its ID.
            See [AG Grid Row Reference ](https://www.ag-grid.com/javascript-data-grid/row-object/) for a list of methods.
            The method call can be awaited to get the result, or it can be executed without waiting for a response.

            Args:
                - row_id (str): The ID of the row as defined by the `getRowId` option.
                - name (str): The name of the method to be executed.
                - *args: Additional arguments to pass to the method.
                - timeout (float, optional): The timeout in seconds for waiting for a response. Defaults to 1 second.
                - check_interval (float, optional): The interval in seconds to check for a response. Defaults to 0.01 seconds.

            Returns:
                - AwaitableResponse: An AwaitableResponse object that can be awaited to get the result of the method call.

            Raises:
                - TimeoutError: If the method call times out and no response is received within the specified timeout.

            Example:
                # Create an instance of AGGrid
                grid = AGGrid()

                # Run the 'selectNode' method on a specific row with ID 'row1'
                response = grid.run_row_method('row1', 'selectNode')

                # Await the response to get the result
                result = await response

            See Also:
                - [AG Grid Row Reference](https://www.ag-grid.com/javascript-data-grid/row-object/): A list of available methods for AG Grid rows.
            """
            return self.run_method('run_row_method', row_id, name, *args, timeout=timeout, check_interval=check_interval)

    async def get_selected_rows(self) -> List[Dict]:
            """Get the currently selected rows.

            This method retrieves the currently selected rows in the AG Grid component.
            It is especially useful when the grid is configured with `rowSelection: 'multiple'`.

            Args:
            
                None

            Returns:
                List[Dict]: A list of dictionaries representing the selected row data.
            
            Raises:
                None

            Example:
                ```
                grid = AGGrid()
                selected_rows = await grid.get_selected_rows()
                for row in selected_rows:
                    print(row)
                ```

            See Also:
                - [AG Grid API - getSelectedRows](https://www.ag-grid.com/javascript-data-grid/row-selection/#reference-selection-getSelectedRows)
            """
            result = await self.run_grid_method('getSelectedRows')
            return cast(List[Dict], result)

    async def get_selected_row(self) -> Optional[Dict]:
            """Get the single currently selected row.

            This method is especially useful when the grid is configured with `rowSelection: 'single'`.

            Returns:
                - Optional[Dict]: Row data of the first selection if any row is selected, otherwise `None`.

            Raises:
                None

            Examples:
                Example usage of `get_selected_row`:

                ```python
                grid = AGGrid()
                row = await grid.get_selected_row()
                if row:
                    print(f"Selected row: {row}")
                else:
                    print("No row selected.")
                ```

            Notes:
                - This method assumes that the grid is configured with `rowSelection: 'single'`.
                - If multiple rows are selected, only the first selected row will be returned.
                - If no row is selected, `None` will be returned.
            """
            rows = await self.get_selected_rows()
            return rows[0] if rows else None

    async def get_client_data(self, *, timeout: float = 1, check_interval: float = 0.01) -> List[Dict]:
            """Get the data from the client including any edits made by the client.

            This method retrieves the data from the client-side AG Grid component, including any edits made by the user.
            It is particularly useful when the grid is configured with `'editable': True`.

            See [AG Grid API ](https://www.ag-grid.com/javascript-data-grid/accessing-data/) for more information.
            
            The method uses JavaScript code executed on the client-side to retrieve the row data from the AG Grid component.
            It iterates over each node in the grid and extracts the data associated with each node.

            Note:
                - When editing a cell, the row data is not updated until the cell exits the edit mode.
                  This behavior can be changed by setting `stopEditingWhenCellsLoseFocus: True`.
                - The method relies on the `run_javascript` method of the `client` object to execute the JavaScript code.

            Args:
                - timeout (float, optional): The maximum time to wait for a response from the client, in seconds.
                                          Defaults to 1 second.
                - check_interval (float, optional): The interval at which to check for a response from the client, in seconds.
                                                  Defaults to 0.01 seconds.

            Returns:
                - List[Dict]: A list of dictionaries representing the row data.
                            Each dictionary contains the data associated with a single row in the AG Grid component.

            Raises:
                TimeoutError: If the client does not respond within the specified timeout period.

            Example:
                # Create an instance of the AGGrid class
                grid = AGGrid()

                # Configure the grid with editable mode
                grid.set_config({'editable': True})

                # Get the data from the client
                data = await grid.get_client_data()

                # Process the data
                for row in data:
                    # Access the values of each column in the row
                    column1_value = row['column1']
                    column2_value = row['column2']
                    # Perform further processing on the row data

            See Also:
                - [AG Grid API](https://www.ag-grid.com/javascript-data-grid/accessing-data/):
                  Official documentation for accessing data in AG Grid.
                - `run_javascript` method of the `client` object:
                  Documentation for the method used to execute JavaScript code on the client-side.
            """
            result = await self.client.run_javascript(f'''
                const rowData = [];
                getElement({self.id}).gridOptions.api.forEachNode(node => rowData.push(node.data));
                return rowData;
            ''', timeout=timeout, check_interval=check_interval)
            return cast(List[Dict], result)    

    async def load_client_data(self) -> None:
            """Obtain client data and update the element's row data with it.

            This method is responsible for obtaining the client data and updating the row data of the element with it.
            It synchronizes any edits made by the client in editable cells to the server.

            Note:
                - When editing a cell, the row data is not updated until the cell exits the edit mode.
                - The row data is not updated when the cell loses focus, unless `stopEditingWhenCellsLoseFocus: True` is set.

            Returns:
                None

            Raises:
                Any exceptions raised during the execution of this method will be propagated.

            Usage:
                1. Call this method to obtain the client data and update the row data of the element.
                2. This method should be called asynchronously using the `await` keyword.

            Example:
                ```python
                await self.load_client_data()
                ```
            """
            client_row_data = await self.get_client_data()
            self.options['rowData'] = client_row_data
            self.update()
