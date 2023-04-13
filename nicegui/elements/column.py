from ..element import Element


class Column(Element):

    def __init__(self) -> None:
        '''Column Element

        Provides a container which arranges its child in a column.
        '''
        super().__init__('div')
        self._classes = ['nicegui-column']
