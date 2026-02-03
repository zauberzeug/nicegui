import importlib.util
from typing import TYPE_CHECKING, Literal, cast

from typing_extensions import Self

from ... import helpers, optional_features
from ...awaitable_response import AwaitableResponse
from ...defaults import DEFAULT_PROP, resolve_defaults
from ...dependencies import register_importmap_override
from ...element import Element

if importlib.util.find_spec('pandas'):
    optional_features.register('pandas')
    if TYPE_CHECKING:
        import pandas as pd

if importlib.util.find_spec('polars'):
    optional_features.register('polars')
    if TYPE_CHECKING:
        import polars as pl


class AgGrid(Element, component='aggrid.js', esm={'nicegui-aggrid': 'dist'}, default_classes='nicegui-aggrid'):

    @resolve_defaults
    def __init__(self,
                 options: dict, *,
                 html_columns: list[int] = DEFAULT_PROP | [],
                 theme: Literal['quartz', 'balham', 'material', 'alpine'] | None = None,
                 auto_size_columns: bool = True,
                 modules: Literal['community', 'enterprise'] | list[str] = 'community',
                 ) -> None:
        """AG Grid

        An element to create a grid using `AG Grid <https://www.ag-grid.com/>`_.
        Updates can be pushed to the grid by updating the ``options`` property.

        The methods ``run_grid_method`` and ``run_row_method`` can be used to interact with the AG Grid instance on the client.

        :param options: dictionary of AG Grid options
        :param html_columns: list of columns that should be rendered as HTML (default: ``[]``)
        :param theme: AG Grid theme "quartz", "balham", "material", or "alpine" (default: ``options['theme']`` or "quartz")
        :param auto_size_columns: whether to automatically resize columns to fit the grid width (default: ``True``)
        :param modules: either "community", "enterprise", or a list of `AG Grid Modules <https://www.ag-grid.com/javascript-data-grid/modules/>`_ (default: "community")
        """
        if not isinstance(modules, list):
            modules = [f'All{modules.capitalize()}Module']

        self._migrate_deprecated_checkbox_renderer(options)  # DEPRECATED: remove in NiceGUI 4.0

        super().__init__()
        self._props['options'] = {
            'theme': theme or 'quartz',
            **({'autoSizeStrategy': {'type': 'fitGridWidth'}} if auto_size_columns else {}),
            **options,
        }
        self._props['html-columns'] = html_columns[:]
        self._update_method = 'update_grid'
        self._props['modules'] = modules[:]

        self._props.add_rename('html_columns', 'html-columns')  # DEPRECATED: remove in NiceGUI 4.0

    @staticmethod
    def _migrate_deprecated_checkbox_renderer(options: dict) -> None:
        """Migrate deprecated checkboxRenderer to agCheckboxCellRenderer and warn the user."""
        migrated = False
        for col in options.get('columnDefs', []):
            if col.get('cellRenderer') == 'checkboxRenderer':
                del col['cellRenderer']
                col['cellDataType'] = 'boolean'
                col['editable'] = True
                migrated = True
        if migrated:
            helpers.warn_once(
                "AG Grid: 'checkboxRenderer' is deprecated.\n"
                'Your code currently contains:\n'
                "    'cellRenderer': 'checkboxRenderer',\n"
                'But the native renderer is preferred for accessibility and styling:\n'
                "    'cellDataType': 'boolean',\n"
                "    'editable': True,\n"
                'Please migrate ASAP as the backwards-compatibility will be removed in NiceGUI 4.0.'
            )

    @classmethod
    def from_pandas(cls,
                    df: 'pd.DataFrame', *,
                    html_columns: list[int] = [],  # noqa: B006
                    theme: Literal['quartz', 'balham', 'material', 'alpine'] | None = None,
                    auto_size_columns: bool = True,
                    options: dict = {},  # noqa: B006
                    modules: Literal['community', 'enterprise'] | list[str] = 'community',
                    ) -> Self:
        """Create an AG Grid from a Pandas DataFrame.

        Note:
        If the DataFrame contains non-serializable columns of type ``datetime64[ns]``, ``timedelta64[ns]``, ``complex128`` or ``period[M]``,
        they will be converted to strings.
        To use a different conversion, convert the DataFrame manually before passing it to this method.
        See `issue 1698 <https://github.com/zauberzeug/nicegui/issues/1698>`_ for more information.

        :param df: Pandas DataFrame
        :param html_columns: list of columns that should be rendered as HTML (default: ``[]``, *added in version 2.19.0*)
        :param theme: AG Grid theme "quartz", "balham", "material", or "alpine" (default: ``options['theme']`` or "quartz")
        :param auto_size_columns: whether to automatically resize columns to fit the grid width (default: ``True``)
        :param options: dictionary of additional AG Grid options
        :param modules: either "community", "enterprise", or a list of `AG Grid Modules <https://www.ag-grid.com/javascript-data-grid/modules/>`_ (default: "community")
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
            'theme': theme or options.get('theme', 'quartz'),
        }, html_columns=html_columns, theme=theme, auto_size_columns=auto_size_columns, modules=modules)

    @classmethod
    def from_polars(cls,
                    df: 'pl.DataFrame', *,
                    html_columns: list[int] = [],  # noqa: B006
                    theme: Literal['quartz', 'balham', 'material', 'alpine'] | None = None,
                    auto_size_columns: bool = True,
                    options: dict = {},  # noqa: B006
                    modules: Literal['community', 'enterprise'] | list[str] = 'community',
                    ) -> Self:
        """Create an AG Grid from a Polars DataFrame.

        If the DataFrame contains non-UTF-8 datatypes, they will be converted to strings.
        To use a different conversion, convert the DataFrame manually before passing it to this method.

        *Added in version 2.7.0*

        :param df: Polars DataFrame
        :param html_columns: list of columns that should be rendered as HTML (default: ``[]``, *added in version 2.19.0*)
        :param theme: AG Grid theme "quartz", "balham", "material", or "alpine" (default: ``options['theme']`` or "quartz")
        :param auto_size_columns: whether to automatically resize columns to fit the grid width (default: ``True``)
        :param options: dictionary of additional AG Grid options
        :param modules: either "community", "enterprise", or a list of `AG Grid Modules <https://www.ag-grid.com/javascript-data-grid/modules/>`_ (default: "community")
        :return: AG Grid element
        """
        return cls({
            'columnDefs': [{'field': str(col)} for col in df.columns],
            'rowData': df.to_dicts(),
            'suppressFieldDotNotation': True,
            **options,
            'theme': theme or options.get('theme', 'quartz'),
        }, html_columns=html_columns, theme=theme, auto_size_columns=auto_size_columns, modules=modules)

    @property
    def options(self) -> dict:
        """The options dictionary."""
        return self._props['options']

    @options.setter
    def options(self, value: dict) -> None:
        self._props['options'] = value

    @property
    def html_columns(self) -> list[int]:
        """The list of columns that should be rendered as HTML."""
        return self._props['html-columns']

    @html_columns.setter
    def html_columns(self, value: list[int]) -> None:
        self._props['html-columns'] = value[:]

    @property
    def theme(self) -> Literal['quartz', 'balham', 'material', 'alpine'] | None:
        """The AG Grid theme."""
        return self._props['options'].get('theme')

    @theme.setter
    def theme(self, value: Literal['quartz', 'balham', 'material', 'alpine'] | None) -> None:
        self._props['options']['theme'] = value

    @property
    def auto_size_columns(self) -> bool:
        """Whether to automatically resize columns to fit the grid width."""
        return self._props['options'].get('autoSizeStrategy', {}).get('type') == 'fitGridWidth'

    @auto_size_columns.setter
    def auto_size_columns(self, value: bool) -> None:
        if value and not self.auto_size_columns:
            self._props['options']['autoSizeStrategy'] = {'type': 'fitGridWidth'}
        if not value and self.auto_size_columns:
            self._props['options'].pop('autoSizeStrategy')

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

    async def get_selected_rows(self) -> list[dict]:
        """Get the currently selected rows.

        This method is especially useful when the grid is configured with ``rowSelection: 'multiple'``.

        See `AG Grid API <https://www.ag-grid.com/javascript-data-grid/row-selection/#reference-selection-getSelectedRows>`_ for more information.

        :return: list of selected row data
        """
        result = await self.run_grid_method('getSelectedRows')
        return cast(list[dict], result)

    async def get_selected_row(self) -> dict | None:
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
    ) -> list[dict]:
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
        return cast(list[dict], result)

    async def load_client_data(self) -> None:
        """Obtain client data and update the element's row data with it.

        This syncs edits made by the client in editable cells to the server.

        Note that when editing a cell, the row data is not updated until the cell exits the edit mode.
        This does not happen when the cell loses focus, unless ``stopEditingWhenCellsLoseFocus: True`` is set.
        """
        client_row_data = await self.get_client_data()
        self.options['rowData'] = client_row_data

    @staticmethod
    def set_module_source(url: str) -> None:
        """Override the ESM module URL for all AG Grid elements.

        This sets a global import map override, affecting all pages and clients.
        Use this to switch to AG Grid Enterprise or a self-hosted bundle.

        :param url: the ESM module URL (e.g., "https://cdn.jsdelivr.net/npm/ag-grid-enterprise@34.2.0/+esm")
        """
        register_importmap_override('nicegui-aggrid', url)
