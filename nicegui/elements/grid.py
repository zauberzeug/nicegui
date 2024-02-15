from typing import Optional

from ..element import Element


class Grid(Element):
    """A container element that arranges its child elements in a grid.

    The Grid element provides a way to organize child elements in a grid layout.
    It allows you to specify the number of rows and columns in the grid, and
    automatically adjusts the size of each cell to fit its content.

    Attributes:
        - rows (Optional[int]): The number of rows in the grid.
        - columns (Optional[int]): The number of columns in the grid.

    """

    def __init__(self,
                 *,
                 rows: Optional[int] = None,
                 columns: Optional[int] = None,
                 ) -> None:
        """Initialize the Grid element.

        Args:
            rows (Optional[int]): The number of rows in the grid.
            columns (Optional[int]): The number of columns in the grid.
        """
        super().__init__('div')
        self._classes.append('nicegui-grid')
        if rows is not None:
            self._style['grid-template-rows'] = f'repeat({rows}, minmax(0, 1fr))'
        if columns is not None:
            self._style['grid-template-columns'] = f'repeat({columns}, minmax(0, 1fr))'
