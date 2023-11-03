from ..element import Element


class Row(Element):

    def __init__(self, *, wrap: bool = True) -> None:
        """Row Element

        Provides a container which arranges its child in a row.

        :param wrap: whether to wrap the content (default: `True`)
        """
        super().__init__('div')
        self._classes.append('nicegui-row')

        if wrap:
            self._classes.append('wrap')
