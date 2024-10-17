from typing import Optional, Union

from ..element import Element


class Grid(Element, default_classes='nicegui-grid'):

    def __init__(self,
                 *,
                 rows: Optional[Union[int, str]] = None,
                 columns: Optional[Union[int, str]] = None,
                 ) -> None:
        """Grid Element

        Provides a container which arranges its child in a grid.

        :param rows: number of rows in the grid or a string with the grid-template-rows CSS property (e.g. 'auto 1fr')
        :param columns: number of columns in the grid or a string with the grid-template-columns CSS property (e.g. 'auto 1fr')
        """
        super().__init__('div')

        if isinstance(rows, int):
            self._style['grid-template-rows'] = f'repeat({rows}, minmax(0, 1fr))'
        elif isinstance(rows, str):
            self._style['grid-template-rows'] = rows

        if isinstance(columns, int):
            self._style['grid-template-columns'] = f'repeat({columns}, minmax(0, 1fr))'
        elif isinstance(columns, str):
            self._style['grid-template-columns'] = columns
