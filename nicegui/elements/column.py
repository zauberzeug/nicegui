from ..element import Element


class Column(Element):

    def __init__(self) -> None:
        '''Column Element

        Provides a container which arranges its child in a row.
        '''
        super().__init__('div')
        self.classes('column items-start gap-4')
