from ..element import Element


class Separator(Element):

    def __init__(self) -> None:
        """Separator

        A separator for cards, menus and other component containers.
        """
        super().__init__('q-separator')
        self._classes = ['nicegui-separator']
