from ..element import Element


class Row(Element):

    def __init__(self) -> None:
        '''Row Element

        Provides a container which arranges its child in a row.
        '''
        super().__init__('div')
        self.classes('row items-start gap-4')
