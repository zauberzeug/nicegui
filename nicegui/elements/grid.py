from typing import Optional

from ..element import Element


class Grid(Element):

    def __init__(self,
                 rows: Optional[int] = None,
                 columns: Optional[int] = None,
                 ) -> None:
        '''Grid Element

        Provides a container which arranges its child in a grid.

        :param rows: number of rows in the grid
        :param columns: number of columns in the grid
        '''
        super().__init__('div')
        self._classes = ['nicegui-grid']
        if rows is not None:
            self._style['grid-template-rows'] = f'repeat({rows}, minmax(0, 1fr))'
        if columns is not None:
            self._style['grid-template-columns'] = f'repeat({columns}, minmax(0, 1fr))'
