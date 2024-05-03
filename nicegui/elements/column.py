from ..element import Element


class Column(Element):

    def __init__(self, *, wrap: bool = False) -> None:
        """Column Element

        Provides a container which arranges its child in a column.

        :param wrap: whether to wrap the content (default: `False`)
        """
        super().__init__('div')
        self._classes.append('nicegui-column')

        if wrap:
            self._style['flex-wrap'] = 'wrap'
